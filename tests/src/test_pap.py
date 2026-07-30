import pytest

from txt2stix.pap_levels import PAP_LEVEL, PAP_EXTENSION_DEFINITION_ID

# https://github.com/oasis-open/cti-stix-common-objects/blob/main/extension-definition-specifications/pap-marking-definition-f8d/extension-definition--f8d78575-edfd-406e-8e84-6162a8450f5b.json
OFFICIAL_IDS = {
    "clear": "marking-definition--ad15a0cd-55b6-4588-a14c-a66105329b92",
    "green": "marking-definition--c43594d1-4b11-4c59-93ab-1c9b14d53ce9",
    "amber": "marking-definition--60f8932b-e51e-4458-b265-a2e8be9a80ab",
    "red": "marking-definition--740d36e5-7714-4c30-961a-3ae632ceee0e",
    "white": "marking-definition--a3bea94c-b469-41dc-9cfe-d6e7daba7730",
}


def test_pap_extension_definition_id():
    assert (
        PAP_EXTENSION_DEFINITION_ID
        == "extension-definition--f8d78575-edfd-406e-8e84-6162a8450f5b"
    )


def test_pap_levels():
    assert list(PAP_LEVEL.levels()) == ["clear", "green", "amber", "red", "white"]
    assert all(
        item.value.id.startswith("marking-definition--") for item in PAP_LEVEL
    )


def test_pap_matches_official_oasis_ids():
    for name, expected_id in OFFICIAL_IDS.items():
        assert PAP_LEVEL.levels()[name].value.id == expected_id


def test_pap_values_are_unique_marking_definitions():
    ids = {item.value.id for item in PAP_LEVEL}
    assert len(ids) == len(list(PAP_LEVEL))


@pytest.mark.parametrize(
    ("level", "expected"),
    [
        ("clear", PAP_LEVEL.CLEAR),
        ("CLEAR", PAP_LEVEL.CLEAR),
        ("green", PAP_LEVEL.GREEN),
        ("amber", PAP_LEVEL.AMBER),
        ("red", PAP_LEVEL.RED),
        ("white", PAP_LEVEL.WHITE),
        (PAP_LEVEL.RED, PAP_LEVEL.RED),
    ],
)
def test_pap_get(level, expected):
    assert PAP_LEVEL.get(level) == expected


def test_pap_get_invalid():
    with pytest.raises(KeyError):
        PAP_LEVEL.get("black")


def test_pap_extension_property():
    for name, level in PAP_LEVEL.levels().items():
        assert level.value.extensions[PAP_EXTENSION_DEFINITION_ID]["pap"] == name
        assert level.value.extensions[PAP_EXTENSION_DEFINITION_ID]["extension_type"] == "property-extension"
        assert level.value.name == f"PAP:{name.upper()}"


def test_pap_marking_definitions_have_no_definition_type():
    # PAP marking-definitions use the `extensions` property exclusively;
    # `definition_type`/`definition` MUST NOT be present per the OASIS spec.
    for level in PAP_LEVEL:
        assert "definition_type" not in level.value
        assert "definition" not in level.value
