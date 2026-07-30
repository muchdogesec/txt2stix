from datetime import datetime
from pathlib import Path
from unittest import mock
import os

import pytest

from txt2stix import get_all_extractors
from txt2stix.ai_extractor.utils import DescribesIncident
from txt2stix.bundler import txt2stixBundler
from txt2stix.txt2stix import parse_extractors_globbed, parse_model, run_txt2stix

from txt2stix.ai_extractor.utils import (
    AttackFlowList,
    DescribesIncident,
)

all_extractors = get_all_extractors()

TEST_AI_MODEL = os.getenv("TEST_AI_MODEL")

AI_GENERATED_REPORTS_DIR = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "manually_generated_reports"
    / "ai_generated"
)


def new_bundler():
    return txt2stixBundler(
        name="test_indicator.py",
        identity=None,
        tlp_level="red",
        description="",
        confidence=None,
        extractors=None,
        labels=None,
        created=datetime(2020, 1, 1),
    )


mock_bundler = new_bundler()


def as_python(obj):
    import json
    from stix2.serialization import serialize

    return json.loads(serialize(obj))


@mock.patch("txt2stix.txt2stix.validate_token_count")
def test_content_check_param(mock_validate_token_count, subtests):
    """Test the run_txt2stix function"""
    preprocessed_text = "192.168.0.1"
    mock_validate_token_count.return_value = True
    mock_extractors_map = parse_extractors_globbed(
        "extractor",
        all_extractors,
        "pattern_ipv4_address_only,pattern_domain_name_only",
    )
    incident_classifications = ["Class 1", "Class 2", "class 3"]

    with (
        subtests.test(
            "check_content", ai_extract_if_no_incidence=False, describes_incident=False
        ),
        mock.patch(
            "txt2stix.ai_extractor.base.BaseAIExtractor.check_content"
        ) as mock_check_content,
    ):
        bundler = new_bundler()
        assert bundler.report["confidence"] is None
        mock_check_content.return_value = DescribesIncident(
            describes_incident=False,
            explanation="some bs",
            incident_classification=[],
            summary="The summary",
            threat_score=31,
        )
        data = run_txt2stix(
            bundler,
            preprocessed_text,
            mock_extractors_map,
            ai_content_check_provider=parse_model(TEST_AI_MODEL),
            ai_extract_if_no_incidence=False,
        )
        assert data.content_check.describes_incident == False
        assert data.content_check.threat_score == 31
        assert (
            bundler.report["confidence"] == 31
        ), "report.confidence should be replaced by threat_score when confidence is None"
        assert (
            data.extractions == None
        ), "extraction should not happen when check_content.describes_incident is False"
        mock_check_content.assert_called_once()
        mock_validate_token_count.assert_called_once()

    mock_validate_token_count.reset_mock()

    with (
        subtests.test(
            "check_content", describes_incident=False, ai_extract_if_no_incidence=True
        ),
        mock.patch(
            "txt2stix.ai_extractor.base.BaseAIExtractor.check_content"
        ) as mock_check_content,
        mock.patch(
            "txt2stix.txt2stix.txt2stixBundler.add_summary"
        ) as mock_bundle__add_summary,
    ):
        bundler = new_bundler()
        assert bundler.report["confidence"] is None
        mock_check_content.return_value = DescribesIncident(
            describes_incident=False,
            explanation="some bs",
            incident_classification=[],
            summary="The summary",
            threat_score=47,
        )
        data = run_txt2stix(
            bundler,
            preprocessed_text,
            mock_extractors_map,
            ai_content_check_provider=parse_model(TEST_AI_MODEL),
            ai_extract_if_no_incidence=True,
        )
        assert data.content_check.describes_incident == False
        assert data.content_check.threat_score == 47
        assert (
            bundler.report["confidence"] == 47
        ), "report.confidence should be replaced by threat_score when confidence is None"
        assert (
            data.extractions
        ), "extraction should happen when check_content.describes_incident is False but ai_extract_if_no_incidence is True"
        mock_check_content.assert_called_once()
        mock_validate_token_count.assert_called_once()
        mock_bundle__add_summary.assert_called_once_with(
            "The summary", parse_model(TEST_AI_MODEL).extractor_name
        )
        assert {
            "source_name": "txt2stix_describes_incident",
            "description": "false",
            "external_id": parse_model(TEST_AI_MODEL).extractor_name,
        } in as_python(bundler.report["external_references"])

    mock_validate_token_count.reset_mock()

    with (
        subtests.test("check_content", describes_incident=True),
        mock.patch(
            "txt2stix.ai_extractor.base.BaseAIExtractor.check_content"
        ) as mock_check_content,
        mock.patch(
            "txt2stix.txt2stix.txt2stixBundler.add_summary"
        ) as mock_bundle__add_summary,
    ):
        bundler = new_bundler()
        assert bundler.report["confidence"] is None
        mock_check_content.return_value = DescribesIncident(
            describes_incident=True,
            explanation="some bs",
            incident_classification=incident_classifications,
            summary="The summary",
            threat_score=85,
        )
        data = run_txt2stix(
            bundler,
            preprocessed_text,
            mock_extractors_map,
            ai_content_check_provider=parse_model(TEST_AI_MODEL),
        )
        assert data.content_check.describes_incident == True
        assert data.content_check.threat_score == 85
        assert (
            bundler.report["confidence"] == 85
        ), "report.confidence should be replaced by threat_score when confidence is None"
        assert (
            data.extractions
        ), "extraction should happen when check_content.describes_incident is True"
        mock_check_content.assert_called_once()
        mock_validate_token_count.assert_called_once()
        for classification in incident_classifications:
            assert (
                f"classification.{classification}".lower() in bundler.report["labels"]
            )
        mock_bundle__add_summary.assert_called_once_with(
            "The summary", parse_model(TEST_AI_MODEL).extractor_name
        )
        assert {
            "source_name": "txt2stix_describes_incident",
            "description": "true",
            "external_id": parse_model(TEST_AI_MODEL).extractor_name,
        } in as_python(bundler.report["external_references"])

    mock_validate_token_count.reset_mock()

    with (
        subtests.test("no_check_content"),
        mock.patch(
            "txt2stix.ai_extractor.base.BaseAIExtractor.check_content"
        ) as mock_check_content,
    ):
        bundler = new_bundler()
        assert bundler.report["confidence"] is None
        mock_check_content.return_value = DescribesIncident(
            describes_incident=True,
            explanation="some bs",
            incident_classification=["yes"],
            summary="The summary",
            threat_score=50,
        )
        data = run_txt2stix(bundler, preprocessed_text, mock_extractors_map)
        assert data.content_check == None, "content_check should be nil"
        assert (
            data.extractions
        ), "extraction should happen when check_content is disabled"
        mock_check_content.assert_not_called()
        mock_validate_token_count.assert_not_called()
        assert (
            bundler.report["confidence"] is None
        ), "report.confidence should remain None when content_check is not used"

    mock_validate_token_count.reset_mock()

    with (
        subtests.test("check_content", confidence_preset=0),
        mock.patch(
            "txt2stix.ai_extractor.base.BaseAIExtractor.check_content"
        ) as mock_check_content,
        mock.patch(
            "txt2stix.txt2stix.txt2stixBundler.add_summary"
        ) as mock_bundle__add_summary,
    ):
        bundler = new_bundler()
        bundler.report["confidence"] = 0
        mock_check_content.return_value = DescribesIncident(
            describes_incident=True,
            explanation="some bs",
            incident_classification=[],
            summary="The summary",
            threat_score=75,
        )
        data = run_txt2stix(
            bundler,
            preprocessed_text,
            mock_extractors_map,
            ai_content_check_provider=parse_model(TEST_AI_MODEL),
        )
        assert data.content_check.threat_score == 75
        assert (
            bundler.report["confidence"] == 0
        ), "report.confidence should NOT be replaced when already set to 0"

    mock_validate_token_count.reset_mock()

    with (
        subtests.test("check_content", confidence_preset=60),
        mock.patch(
            "txt2stix.ai_extractor.base.BaseAIExtractor.check_content"
        ) as mock_check_content,
        mock.patch(
            "txt2stix.txt2stix.txt2stixBundler.add_summary"
        ) as mock_bundle__add_summary,
    ):
        bundler = new_bundler()
        bundler.report["confidence"] = 60
        mock_check_content.return_value = DescribesIncident(
            describes_incident=True,
            explanation="some bs",
            incident_classification=[],
            summary="The summary",
            threat_score=90,
        )
        data = run_txt2stix(
            bundler,
            preprocessed_text,
            mock_extractors_map,
            ai_content_check_provider=parse_model(TEST_AI_MODEL),
        )
        assert data.content_check.threat_score == 90
        assert (
            bundler.report["confidence"] == 60
        ), "report.confidence should NOT be replaced when already set to 60"


@mock.patch("txt2stix.txt2stix.attack_flow.extract_attack_flow_and_navigator")
def test_attack_flow_or_nav__no_preset_flow(mock_extract_attack_flow, subtests):
    preprocessed_text = "192.168.0.1"
    mock_extractors_map = parse_extractors_globbed(
        "extractor",
        all_extractors,
        "pattern_ipv4_address_only,pattern_domain_name_only",
    )
    extractor = parse_model(TEST_AI_MODEL)
    mock_extract_attack_flow.return_value = "a", "b"

    with subtests.test("neither true"):
        retval = run_txt2stix(
            mock_bundler,
            preprocessed_text,
            mock_extractors_map,
            ai_settings_relationships=parse_model(TEST_AI_MODEL),
        )
        mock_extract_attack_flow.assert_not_called()
        assert retval.attack_flow == None, "attack_flow should not run"

    with subtests.test(
        "both true", ai_create_attack_flow=True, ai_create_attack_navigator_layer=True
    ):
        retval = run_txt2stix(
            mock_bundler,
            preprocessed_text,
            mock_extractors_map,
            ai_settings_relationships=extractor,
            ai_create_attack_flow=True,
            ai_create_attack_navigator_layer=True,
        )
        mock_extract_attack_flow.assert_called_once_with(
            mock_bundler, preprocessed_text, True, True, extractor, flow=None
        )
        assert retval.attack_flow == "a"
        assert retval.navigator_layer == "b"

    mock_extract_attack_flow.reset_mock()

    with subtests.test(
        "only flow", ai_create_attack_flow=True, ai_create_attack_navigator_layer=False
    ):
        retval = run_txt2stix(
            mock_bundler,
            preprocessed_text,
            mock_extractors_map,
            ai_settings_relationships=extractor,
            ai_create_attack_flow=True,
            ai_create_attack_navigator_layer=False,
        )
        mock_extract_attack_flow.assert_called_once_with(
            mock_bundler, preprocessed_text, True, False, extractor, flow=None
        )
        assert retval.attack_flow == "a"
        assert retval.navigator_layer == "b"

    mock_extract_attack_flow.reset_mock()

    with subtests.test(
        "only nav", ai_create_attack_flow=False, ai_create_attack_navigator_layer=True
    ):
        retval = run_txt2stix(
            mock_bundler,
            preprocessed_text,
            mock_extractors_map,
            ai_settings_relationships=extractor,
            ai_create_attack_flow=False,
            ai_create_attack_navigator_layer=True,
        )
        mock_extract_attack_flow.assert_called_once_with(
            mock_bundler, preprocessed_text, False, True, extractor, flow=None
        )
        assert retval.attack_flow == "a"
        assert retval.navigator_layer == "b"


@mock.patch("txt2stix.txt2stix.extract_relationships")
def test_relationship_mode(mock_extract_relationships, subtests):
    mock_extractors_map = parse_extractors_globbed(
        "extractor",
        all_extractors,
        "pattern_ipv4_address_only,pattern_domain_name_only",
    )
    preprocessed_text = "192.168.0.1"
    mock_extract_relationships.return_value = []

    with subtests.test("mode_standard"):
        retval = run_txt2stix(
            mock_bundler,
            preprocessed_text,
            mock_extractors_map,
            ai_settings_relationships=parse_model(TEST_AI_MODEL),
            relationship_mode="standard",
        )
        mock_extract_relationships.assert_not_called()
        assert (
            retval.relationships == None
        ), "extract_relationships_with_ai should not run"

    with subtests.test("mode_ai"):
        retval = run_txt2stix(
            mock_bundler,
            preprocessed_text,
            mock_extractors_map,
            ai_settings_relationships=parse_model(TEST_AI_MODEL),
            relationship_mode="ai",
        )
        mock_extract_relationships.assert_called_once()
        assert retval.relationships != None, "extract_relationships_with_ai should run"


@pytest.mark.parametrize(
    ("filename", "expected_lang"),
    [
        ("report_fr.txt", "fr"),
        ("report_de.txt", "de"),
        ("report_es.txt", "es"),
        ("report_ja.txt", "ja"),
        ("company.txt", "en"),
    ],
)
def test_language_detected_via_langid_without_content_check(filename, expected_lang):
    """When no AI content check provider is used, `lang` should come from py3langid."""
    text = (AI_GENERATED_REPORTS_DIR / filename).read_text()
    bundler = new_bundler()

    data = run_txt2stix(bundler, text, {})

    assert data.language == expected_lang
    assert bundler.report["lang"] == expected_lang


@mock.patch("txt2stix.txt2stix.validate_token_count")
def test_ai_content_check_language_takes_priority_over_langid(
    mock_validate_token_count,
):
    """The AI-determined language should override the py3langid result when both run."""
    preprocessed_text = (AI_GENERATED_REPORTS_DIR / "report_fr.txt").read_text()
    bundler = new_bundler()

    with mock.patch(
        "txt2stix.ai_extractor.base.BaseAIExtractor.check_content"
    ) as mock_check_content:
        mock_check_content.return_value = DescribesIncident(
            describes_incident=True,
            explanation="some bs",
            incident_classification=[],
            summary="The summary",
            threat_score=50,
            language="de",
        )
        data = run_txt2stix(
            bundler,
            preprocessed_text,
            {},
            ai_content_check_provider=parse_model(TEST_AI_MODEL),
        )

    assert (
        data.language == "de"
    ), "AI content check language should take priority over langid"
    assert bundler.report["lang"] == "de"


@mock.patch("txt2stix.txt2stix.validate_token_count")
def test_langid_used_when_ai_content_check_language_empty(mock_validate_token_count):
    """If the AI content check does not return a language, the py3langid result is kept."""
    preprocessed_text = (AI_GENERATED_REPORTS_DIR / "report_fr.txt").read_text()
    bundler = new_bundler()

    with mock.patch(
        "txt2stix.ai_extractor.base.BaseAIExtractor.check_content"
    ) as mock_check_content:
        mock_check_content.return_value = DescribesIncident(
            describes_incident=True,
            explanation="some bs",
            incident_classification=[],
            summary="The summary",
            threat_score=50,
        )
        data = run_txt2stix(
            bundler,
            preprocessed_text,
            {},
            ai_content_check_provider=parse_model(TEST_AI_MODEL),
        )

    assert (
        data.language == "fr"
    ), "langid result should be used when content check does not return a language"
    assert bundler.report["lang"] == "fr"
