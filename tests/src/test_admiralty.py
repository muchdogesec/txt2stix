import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from txt2stix import admiralty
from txt2stix.admiralty import (
    ADMIRALTY_INFORMATION_CREDIBILITY,
    ADMIRALTY_SOURCE_RELIABILITY,
)

BUNDLE_PATH = (
    Path(__file__).resolve().parents[1] / "data" / "admiralty" / "all_objects_bundle.json"
)
BUNDLE_DATA = json.loads(BUNDLE_PATH.read_text())


@pytest.fixture(autouse=True)
def reset_admiralty_cache(monkeypatch):
    admiralty.prepare.cache_clear()
    monkeypatch.setattr(admiralty, "ADMIRALTY__OBJECTS", {})
    yield
    admiralty.prepare.cache_clear()


@pytest.fixture
def mock_bundle_fetch(monkeypatch):
    requested = []

    def get(url, timeout):
        requested.append((url, timeout))
        response = MagicMock()
        response.json.return_value = BUNDLE_DATA
        response.raise_for_status.return_value = None
        return response

    monkeypatch.setattr(admiralty.requests, "get", get)
    return requested


def test_source_reliability_values():
    assert list(ADMIRALTY_SOURCE_RELIABILITY.levels()) == list("ABCDEF")
    assert all(
        item.stix_id.startswith("marking-definition--")
        for item in ADMIRALTY_SOURCE_RELIABILITY
    )
    assert (
        ADMIRALTY_SOURCE_RELIABILITY.get("a").stix_id
        == "marking-definition--cf438540-077a-56c7-b68e-82fcc2bb0208"
    )
    assert [item.stix_id for item in ADMIRALTY_SOURCE_RELIABILITY] == [
        "marking-definition--cf438540-077a-56c7-b68e-82fcc2bb0208",
        "marking-definition--b3cd9dd0-9081-5cbe-84d0-ef5bc11b8b13",
        "marking-definition--3545f856-c5f5-5d2f-a1ae-102e0b6028b2",
        "marking-definition--223ecfcc-22ce-5ece-b91c-a05a53a91959",
        "marking-definition--9eff5f66-33b9-5e54-9868-72179b28ae12",
        "marking-definition--adebda39-90c9-5ac0-9107-c26d86a6c3d8",
    ]


def test_information_credibility_values():
    assert list(ADMIRALTY_INFORMATION_CREDIBILITY.levels()) == [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
    ]
    assert all(
        item.stix_id.startswith("marking-definition--")
        for item in ADMIRALTY_INFORMATION_CREDIBILITY
    )
    assert (
        ADMIRALTY_INFORMATION_CREDIBILITY.get(1).stix_id
        == "marking-definition--2462b621-0825-5879-917c-082e0394bcf4"
    )
    assert [item.stix_id for item in ADMIRALTY_INFORMATION_CREDIBILITY] == [
        "marking-definition--2462b621-0825-5879-917c-082e0394bcf4",
        "marking-definition--9cf59b27-57f8-5250-98f4-16c462d5652c",
        "marking-definition--4c76ec83-d905-5ada-b0bf-8ae2fb9e9f4d",
        "marking-definition--c36a018d-bc8e-57a4-a39d-9e7e31d1bc17",
        "marking-definition--0a48adab-e7d5-5354-8a41-abf199fe2628",
        "marking-definition--2244db4b-ee29-5b8c-bed4-c7ac784c647a",
    ]


def test_marking_value_is_fetched_from_bundle(mock_bundle_fetch):
    member = ADMIRALTY_SOURCE_RELIABILITY.A

    assert member.value.id == member.stix_id
    assert mock_bundle_fetch == [
        (
            "https://downloads.ctibutler.com/admiralty-codes/objects/bundle/all_objects_bundle.json",
            30,
        )
    ]


def test_bundle_is_only_fetched_once(mock_bundle_fetch):
    ADMIRALTY_SOURCE_RELIABILITY.A.value
    ADMIRALTY_SOURCE_RELIABILITY.B.value
    ADMIRALTY_INFORMATION_CREDIBILITY._1.value

    assert len(mock_bundle_fetch) == 1


def test_objects_includes_extension_definition_and_referenced_objects(
    mock_bundle_fetch,
):
    member = ADMIRALTY_SOURCE_RELIABILITY.A
    objects = list(member.objects)

    assert objects[0] is ADMIRALTY_SOURCE_RELIABILITY.extension_definition
    assert objects[0].type == "extension-definition"
    assert objects[-1].id == member.stix_id

    ids = {obj.id for obj in objects}
    assert member.value["created_by_ref"] in ids
    for ref in member.value["object_marking_refs"]:
        if ref in admiralty.ADMIRALTY__OBJECTS:
            assert ref in ids


@pytest.mark.parametrize(
    ("enum", "bad_value"),
    [
        (ADMIRALTY_SOURCE_RELIABILITY, "G"),
        (ADMIRALTY_INFORMATION_CREDIBILITY, 7),
    ],
)
def test_invalid_admiralty_value(enum, bad_value):
    with pytest.raises(KeyError):
        enum.get(bad_value)
