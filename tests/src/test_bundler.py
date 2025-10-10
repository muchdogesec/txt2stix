from unittest.mock import MagicMock, call, patch
import uuid

import pytest
from txt2stix.bundler import txt2stixBundler, TLP_LEVEL
from txt2stix.common import MinorException
from . import utils
from dateutil.parser import parse as parse_date
from stix2 import Identity, Relationship
from stix2extensions import Weakness, PaymentCard

dummy_identity = Identity(
    **{
        "type": "identity",
        "spec_version": "2.1",
        "id": "identity--b1ae1a15-abcd-431e-b990-1b9678f35e15",
        "name": "Test Identity",
    }
)


@pytest.mark.parametrize(
    ["tlp_level", "identity", "created", "modified"],
    [
        ("red", None, None, "2024-01-01T16:00:00.000Z"),
        ("green", None, "2024-10-09T16:00:00.000Z", None),
        ("amber", dummy_identity, None, "2024-01-01T16:00:00.000Z"),
        ("clear", None, "2024-10-09T16:00:00.000Z", "2024-01-01T16:00:00.000Z"),
    ],
)
def test_constructor(tlp_level, identity, created, modified):
    report_id = str(uuid.uuid4())
    bundler = txt2stixBundler(
        "n",
        identity,
        tlp_level,
        "",
        0,
        [],
        [],
        report_id,
        created=created,
        modified=modified,
    )
    assert bundler.tlp_level.name == tlp_level
    assert bundler.report.id == "report--" + report_id
    assert bundler.tlp_level.value["id"] in bundler.report.object_marking_refs
    assert bundler.report.published == bundler.report.created
    if identity:
        assert identity == bundler.identity, "passed identity ignored"
    else:
        assert (
            bundler.identity == bundler.default_identity
        ), "default identity must be used if no identity is passed"
    assert (
        bundler.report.created_by_ref == bundler.identity["id"]
    ), "report not using bundler.identity"
    if not modified:
        assert (
            bundler.report.modified == bundler.report.created
        ), "modified and created should be the same if modified is not passed"
    else:
        assert bundler.report.modified == parse_date(modified)
    if created:
        assert bundler.report.created == parse_date(created)

    assert (
        bundler.identity in bundler.bundle.objects
    ), "identity must be in bundle.objects"
    assert (
        bundler.tlp_level.value in bundler.bundle.objects
    ), "tlp_level marking definition must be in bundle.objects"
    assert bundler.report in bundler.bundle.objects, "report must be in bundle.objects"


@pytest.mark.parametrize(
    "obj",
    [
        Weakness(name="test weakness"),
        PaymentCard(value="1234567891011"),
    ],
)
def test_add_ref(bundler, obj):
    bundler.add_ref(obj)
    assert obj in bundler.bundle.objects
    assert obj.id in bundler.added_objects


def test_add_indicator(bundler):
    mocked_extractor = MagicMock()
    bundler.all_extractors = dict(placeholder_extractor=mocked_extractor)
    mocked_related_refs = MagicMock()
    mocked_observables = MagicMock()
    with (
        patch.object(txt2stixBundler, "new_indicator") as mock_new_indicator,
        patch("txt2stix.bundler.build_observables") as mock_build_observables,
    ):
        extracted_dict = dict(
            type="placeholder_extractor", value="test value", id="extract-19"
        )
        mock_build_observables.return_value = mocked_observables, mocked_related_refs
        bundler.add_indicator(extracted_dict, True)

        mock_new_indicator.assert_called_once_with(
            mocked_extractor, mocked_extractor.stix_mapping, extracted_dict["value"]
        )
        mock_build_observables.assert_called_once_with(
            bundler,
            mocked_extractor.stix_mapping,
            mock_new_indicator.return_value,
            extracted_dict["value"],
            mocked_extractor,
        )
        assert bundler.id_map[extracted_dict["id"]] == mocked_related_refs


def test_add_indicator_sets_id_map():
    extractor = MagicMock()
    extractor.stix_mapping = "domain-name"
    extractor.slug = "testslug"
    extractor.version = "1.0"

    bundler = txt2stixBundler(
        name="Test",
        identity=None,
        tlp_level="red",
        description="desc",
        confidence=20,
        extractors={"domain": extractor},
        labels=[],
    )

    # patch build_observables to return one object
    with patch("txt2stix.bundler.build_observables") as mock_build:
        mock_build.return_value = (
            [
                {
                    "type": "domain-name",
                    "id": "domain-name--926a1335-a4d7-40d3-804c-3aa53da6fc9e",
                    "value": "test.com",
                }
            ],
            ["domain-name--926a1335-a4d7-40d3-804c-3aa53da6fc9e"],
        )

        extracted = {"type": "domain", "value": "test.com", "id": "testid"}
        bundler.add_indicator(extracted, add_standard_relationship=False)

        assert "testid" in bundler.id_map
        assert bundler.id_map["testid"] == [
            "domain-name--926a1335-a4d7-40d3-804c-3aa53da6fc9e"
        ]
        assert (
            "domain-name--926a1335-a4d7-40d3-804c-3aa53da6fc9e" in bundler.id_value_map
        )


def test_add_indicator_raises_minor_exception():
    extractor = MagicMock()
    extractor.stix_mapping = "domain-name"
    extractor.slug = "testslug"
    extractor.version = "1.0"

    bundler = txt2stixBundler(
        name="Test",
        identity=None,
        tlp_level="red",
        description="desc",
        confidence=20,
        extractors={"domain": extractor},
        labels=[],
    )

    # patch build_observables to return one object
    with (
        patch("txt2stix.bundler.build_observables") as mock_build,
        pytest.raises(MinorException),
    ):
        mock_build.return_value = ([], [])

        extracted = {"type": "domain", "value": "test.com", "id": "testid"}
        bundler.add_indicator(extracted, add_standard_relationship=False)


def test_flow_objects(bundler):

    obj = {"id": "indicator--123", "type": "indicator", "name": "x"}
    bundler.flow_objects = [obj, bundler.report]

    assert "indicator--123" in bundler.id_value_map
    assert obj in bundler.bundle.objects
    assert {d["id"] for d in bundler.flow_objects} == {
        "report--d9f3b306-e7fe-4074-b89a-33ce54280718",
        "extension-definition--fb9c968a-745b-4ade-9b25-c324172197f4",
        "identity--d673f8cb-c168-42da-8ed4-0cb26725f86c",
        "indicator--123",
    }


def test_add_standard_relationship(bundler):

    bundler.id_value_map["identity--6493ad42-ec4d-4260-b2e9-3f3a1110193c"] = "valA"
    bundler.id_value_map["phone-number--8764871f-6521-4401-bbf2-a17538435f49"] = "valB"

    bundler.add_standard_relationship(
        "identity--6493ad42-ec4d-4260-b2e9-3f3a1110193c",
        "phone-number--8764871f-6521-4401-bbf2-a17538435f49",
        "xx-related-to",
    )
    assert "relationship--290e1319-7a95-5f51-b2c5-463f896cb35a" in bundler.added_objects

    found = [
        obj
        for obj in bundler.bundle.objects
        if obj["id"] == "relationship--290e1319-7a95-5f51-b2c5-463f896cb35a"
    ][0]
    assert found.description == "valA xx related to valB"
    assert found.relationship_type == "related-to"  # renamed cause invalid
    assert found.source_ref == "identity--6493ad42-ec4d-4260-b2e9-3f3a1110193c"
    assert found.target_ref == "phone-number--8764871f-6521-4401-bbf2-a17538435f49"


@pytest.fixture
def bundler():
    return txt2stixBundler(
        name="Test",
        identity=None,
        tlp_level="amber",
        description="desc",
        confidence=30,
        extractors={},
        labels=[],
        report_id="d9f3b306-e7fe-4074-b89a-33ce54280718",
    )


def test_add_ai_relationship(bundler):
    bundler.id_map["ex1"] = [
        "phone-number--8764871f-6521-4401-bbf2-a17538435f49",
        "indicator--401855b2-bd7a-444f-95b1-723efbdba33b",
    ]
    bundler.id_map["ex2"] = ["identity--6493ad42-ec4d-4260-b2e9-3f3a1110193c"]
    bundler.id_value_map["identity--6493ad42-ec4d-4260-b2e9-3f3a1110193c"] = "valA"
    bundler.id_value_map["phone-number--8764871f-6521-4401-bbf2-a17538435f49"] = "valB"

    with patch.object(
        txt2stixBundler, "add_standard_relationship"
    ) as mock_add_standard_relationship:
        bundler.add_ai_relationship(
            dict(source_ref="ex1", target_ref="ex2", relationship_type="in-use-by")
        )
        mock_add_standard_relationship.assert_any_call(
            "phone-number--8764871f-6521-4401-bbf2-a17538435f49",
            "identity--6493ad42-ec4d-4260-b2e9-3f3a1110193c",
            "in-use-by",
        )
        mock_add_standard_relationship.assert_any_call(
            "indicator--401855b2-bd7a-444f-95b1-723efbdba33b",
            "identity--6493ad42-ec4d-4260-b2e9-3f3a1110193c",
            "in-use-by",
        )


def test_add_summary(bundler):
    summary = "This is a summary"
    bundler.add_summary(summary, "some-random-ai-provider")
    assert bundler.summary == summary
    assert (
        dict(
            external_id="some-random-ai-provider",
            source_name="txt2stix_ai_summary",
            description=summary,
        )
        in bundler.report.external_references
    )


def test_process_observables_and_process_relationships():
    extractor = MagicMock()
    extractor.stix_mapping = "domain-name"
    extractor.slug = "testslug"
    extractor.version = "1.0"

    bundler = txt2stixBundler(
        name="Test Process",
        identity=None,
        tlp_level="amber_strict",
        description="desc",
        confidence=90,
        extractors={"domain": extractor},
        labels=[],
    )

    with patch("txt2stix.bundler.build_observables") as mock_build:
        mock_build.return_value = (
            [
                {
                    "type": "domain-name",
                    "id": "domain-name--5b35eddb-c7fc-43c6-859b-36bb859ebb7c",
                    "value": "foo.com",
                }
            ],
            ["domain-name--5b35eddb-c7fc-43c6-859b-36bb859ebb7c"],
        )
        bundler.process_observables([{"type": "domain", "value": "foo.com"}])

        assert bundler.observables_processed == 1
        assert (
            "domain-name--5b35eddb-c7fc-43c6-859b-36bb859ebb7c" in bundler.id_value_map
        )

    # test process_relationships
    bundler.id_map = {"ai_src": ["a"], "ai_tgt": ["b"]}
    with patch.object(bundler, "add_standard_relationship") as mock_add_rel:
        bundler.process_relationships(
            [
                {
                    "source_ref": "ai_src",
                    "target_ref": "ai_tgt",
                    "relationship_type": "controls",
                }
            ]
        )
        mock_add_rel.assert_called_once_with("a", "b", "controls")


def test_process_observables__records_error():
    extractor = MagicMock()
    extractor.stix_mapping = "domain-name"
    extractor.slug = "testslug"
    extractor.version = "1.0"

    bundler = txt2stixBundler(
        name="Test Process",
        identity=None,
        tlp_level="amber_strict",
        description="desc",
        confidence=90,
        extractors={"domain": extractor},
        labels=[],
    )

    data1 = {"type": "domain", "value": "foo.com"}
    data2 = {"type": "domain", "value": "foo.bar"}
    input_data = [data1, data2]
    with patch.object(
        txt2stixBundler, "add_indicator", side_effect=[Exception, lambda x: x]
    ) as mock_build:
        bundler.process_observables(input_data)
        assert "error" in data1
        assert "error" not in data2


def test_tlp_level_values():
    values = TLP_LEVEL.values()
    assert all(v.type == "marking-definition" for v in values)
    assert len(values) == 5


def test_tlp_level_get_by_enum():
    assert TLP_LEVEL.get(TLP_LEVEL.CLEAR) == TLP_LEVEL.CLEAR


def test_tlp_level_get_by_string():
    assert TLP_LEVEL.get("clear") == TLP_LEVEL.CLEAR
    assert TLP_LEVEL.get("amber_strict") == TLP_LEVEL.AMBER_STRICT
    assert TLP_LEVEL.get("amber+strict") == TLP_LEVEL.AMBER_STRICT
    assert TLP_LEVEL.get("amber-strict") == TLP_LEVEL.AMBER_STRICT


def test_relationship_types(bundler):
    relationship = bundler.new_relationship(
        "email-addr--b2e7528e-0693-57c1-8f2c-5cc679fb61fc",
        "domain-name--8f17bb97-632c-57ca-8856-879a3fd651ce",
        "sent-from",
    )
    assert (
        relationship["relationship_type"] == "related-to"
    ), "unsupported relationship type must be fallback to `related-to`"
    relationship = bundler.new_relationship(
        "domain-name--8f17bb97-632c-57ca-8856-879a3fd651ce",
        "ipv4-addr--b2e7528e-0693-57c1-8f2c-5cc679fb61fc",
        "resolves-to",
    )
    assert (
        relationship["relationship_type"] == "resolves-to"
    ), "relationship type is supported"
