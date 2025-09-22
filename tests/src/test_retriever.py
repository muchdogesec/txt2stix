import pytest
from txt2stix.retriever import _retrieve_stix_objects, retrieve_stix_objects


@pytest.fixture(scope="session")
def f():
    return open("/tmp/ww2.txt", "w+")


@pytest.mark.parametrize(
    ["stix_mapping", "kb_id", "expected_ids"],
    [
        (
            "ctibutler-mitre-attack-enterprise-id",
            "T1548",
            ["attack-pattern--67720091-eee3-4d2d-ae16-8264567f6f5b"],
        ),
        (
            "ctibutler-mitre-attack-mobile-id",
            "S1095",
            ["malware--24c8f6db-71e0-41ef-a1dc-83399a5b17e5"],
        ),
        (
            "ctibutler-mitre-attack-ics-id",
            "M0915",
            ["course-of-action--2f0160b7-e982-49d7-9612-f19b810f1722"],
        ),
        (
            "ctibutler-mitre-capec-id",
            "CAPEC-1",
            ["attack-pattern--92cdcd3d-d734-4442-afc3-4599f261498b"],
        ),
        (
            "ctibutler-mitre-cwe-id",
            "CWE-349",
            ["weakness--b7ed8589-a9c7-586c-a3b6-873ae8f8a9c7"],
        ),
        (
            "ctibutler-mitre-attack-enterprise-name",
            "2015 Ukraine Electric Power Attack",
            ["campaign--46421788-b6e1-4256-b351-f8beffd1afba"],
        ),
        (
            "ctibutler-mitre-attack-enterprise-aliases",
            "Operation Sharpshooter",
            ["campaign--37764c78-2a99-46d1-a7ea-6454b9bf93a0"],
        ),
        (
            "ctibutler-mitre-attack-mobile-name",
            "Impair Defenses",
            ["attack-pattern--20b0931a-8952-42ca-975f-775bad295f1a"],
        ),
        (
            "ctibutler-mitre-attack-mobile-aliases",
            "Storm-0875",
            ["intrusion-set--44d37b89-a739-4810-9111-0d2617a8939b"],
        ),
        (
            "ctibutler-mitre-attack-ics-name",
            "Program Upload",
            ["attack-pattern--3067b85e-271e-4bc5-81ad-ab1a81d411e3"],
        ),
        (
            "ctibutler-mitre-attack-ics-aliases",
            "BROMINE",
            ["intrusion-set--1c63d4ec-0a75-4daa-b1df-0d11af3d3cc1"],
        ),
        (
            "ctibutler-mitre-capec-name",
            "Overflow Buffers",
            ["attack-pattern--77e51461-7843-411c-a90e-852498957f76"],
        ),
        (
            "ctibutler-mitre-cwe-name",
            "Insufficient Encapsulation",
            (
                "weakness--46444370-fe00-5368-8d39-17fc39e4cacb",
                "weakness--b0a3b7a9-fefa-5435-8336-4d2e019597f8",
            ),
        ),
        (
            "ctibutler-location",
            "NG",
            (
                "location--6dbe266a-c149-5ba3-8b39-74f1b5063312",
            ),
        ),
        (
            "ctibutler-mitre-atlas-id",
            "AML.T0050",
            ["attack-pattern--eda10125-6f7d-479f-857a-19ef5d86a961"],
        ),
        (
            "ctibutler-mitre-atlas-name",
            "Defense Evasion",
            ["x-mitre-tactic--c9cf0175-296e-4439-852d-afb870ed5e0c"],
        ),
        (
            "ctibutler-disarm-id",
            "T0131.001",
            ["attack-pattern--db0a00c8-7913-5895-b0a2-a7378eaab591"],
        ),
        (
            "ctibutler-disarm-name",
            "Develop Narratives",
            ["x-mitre-tactic--ec5943c5-cf40-59dd-a7ed-c2175fc9727a"],
        ),
        (
            "vulmatch-cve-id",
            "CVE-2025-7943",
            ["vulnerability--e4390a73-9288-5fd4-aa54-6a9b906bb174"],
        ),
        (
            "vulmatch-cpe-id",
            "cpe:2.3:h:qualcomm:sd821:-:*:*:*:*:*:*:*",
            ["software--0028c970-9268-5988-b941-f6bfc050300a"],
        ),
    ],
)
def test_retrieve_objects(stix_mapping, kb_id, expected_ids, f):
    objects = retrieve_stix_objects(stix_mapping, kb_id)
    assert objects != None
    object_ids = {obj["id"] for obj in objects}
    assert object_ids == set(expected_ids)
