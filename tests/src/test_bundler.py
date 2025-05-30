from unittest.mock import MagicMock, patch
import uuid

import pytest
from txt2stix.bundler import txt2stixBundler, TLP_LEVEL
from . import utils
from dateutil.parser import parse as parse_date
from stix2 import Identity
from stix2extensions import Weakness, BankCard

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
        BankCard(number="1234567891011"),
    ],
)
def test_add_ref(obj):
    bundler = utils.dummy_bundler()
    bundler.add_ref(obj)
    assert obj in bundler.bundle.objects
    assert obj.id in bundler.added_objects


def test_add_indicator():
    bundler = utils.dummy_bundler()
    mocked_extractor = MagicMock()
    bundler.all_extractors = dict(placeholder_extractor=mocked_extractor)
    mocked_related_refs = MagicMock()
    mocked_observables = MagicMock()
    with patch.object(txt2stixBundler, 'new_indicator') as mock_new_indicator, patch(
        "txt2stix.bundler.build_observables"
    ) as mock_build_observables:
        extracted_dict = dict(type='placeholder_extractor', value='test value', id='extract-19')
        mock_build_observables.return_value = mocked_observables, mocked_related_refs
        bundler.add_indicator(extracted_dict, True)


        mock_new_indicator.assert_called_once_with(mocked_extractor, mocked_extractor.stix_mapping, extracted_dict['value'])
        mock_build_observables.assert_called_once_with(bundler, mocked_extractor.stix_mapping, mock_new_indicator.return_value, extracted_dict['value'], mocked_extractor)
        assert bundler.id_map[extracted_dict["id"]] == mocked_related_refs
