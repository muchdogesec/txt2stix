from types import SimpleNamespace
import pytest
from unittest.mock import MagicMock, patch
from stix2extensions._extensions import attack_flow_ExtensionDefinitionSMO

from txt2stix.ai_extractor.utils import AttackFlowList, AttackFlowItem
from txt2stix.attack_flow import (
    create_navigator_layer,
    get_all_tactics,
    get_techniques_from_extracted_objects,
    parse_domain_flow,
    parse_flow,
    extract_attack_flow_and_navigator,
)
from stix2 import Report

from txt2stix.txt2stix import parse_model


def test_parse_flow(dummy_report, dummy_objects, dummy_flow):
    tactics = get_all_tactics()
    techniques = get_techniques_from_extracted_objects(dummy_objects, tactics)
    flow = dummy_flow
    report = dummy_report
    expected_ids = {
        "attack-pattern--1b22b676-9347-4c55-9a35-ef0dc653db5b",
        "x-mitre-tactic--298fe907-7931-4fd2-8131-2814dd493134",
        "attack-action--1fd63972-ef98-5da5-81f5-4090c7dfa585",
        "extension-definition--fb9c968a-745b-4ade-9b25-c324172197f4",
        "attack-pattern--1a80d097-54df-41d8-9d33-34e755ec5e72",
        "report--9c88fbcb-8c0d-4124-868b-3dcb1e9b696c",
        "attack-flow--bb21585c-5f82-55cf-b73d-89b5217ef092",
        "relationship--22e97298-819a-55ac-b57b-2185ffb72c62",
        "x-mitre-tactic--2558fd61-8c75-4730-94c4-11926db2a263",
        "attack-action--c7e06b10-252d-520d-82eb-e32314bbec34",
        "x-mitre-tactic--696af733-728e-49d7-8261-75fdc590f453",
        "x-mitre-tactic--5bc1d813-693e-4823-9961-abf9af4b0e92",
        "attack-pattern--f9e9365a-9ca2-4d9c-8e7c-050d73d1101a",
        "attack-action--51dc1572-cb10-581b-b9ef-9e589615ecaa",
        "relationship--931f6b0d-5136-534a-93bc-8cce065e04dc",
        "attack-pattern--0fe075d5-beac-4d02-b93e-0f874997db72",
        "attack-flow--b48ec5d9-407c-5e4a-a6d0-fe851cd4ea0e",
        "attack-action--e03c89ba-a476-5509-ac0a-049b61514be7",
    }

    flow_objects = parse_flow(report, flow, techniques, tactics)
    assert {obj["id"] for obj in flow_objects} == expected_ids

def test_parse_flow__no_success(dummy_report):
    flow_objects = parse_flow(
        dummy_report,
        AttackFlowList(
            success=False,
            matrix="enterprise",
            items=[],
            tactic_selection=[],
        ),
        None,
        None,
    )
    assert len(flow_objects) == 0


@pytest.mark.parametrize(
    ["domain", "expected_ids"],
    [
        ("mobile-attack", set()),
        [
            "ics-attack",
            {
                "x-mitre-tactic--298fe907-7931-4fd2-8131-2814dd493134",
                "x-mitre-tactic--696af733-728e-49d7-8261-75fdc590f453",
                "attack-pattern--1b22b676-9347-4c55-9a35-ef0dc653db5b",
                "relationship--22e97298-819a-55ac-b57b-2185ffb72c62",
                "attack-action--1fd63972-ef98-5da5-81f5-4090c7dfa585",
                "attack-pattern--0fe075d5-beac-4d02-b93e-0f874997db72",
                "attack-flow--bb21585c-5f82-55cf-b73d-89b5217ef092",
                "attack-action--51dc1572-cb10-581b-b9ef-9e589615ecaa",
            },
        ],
        [
            "enterprise-attack",
            {
                "attack-action--e03c89ba-a476-5509-ac0a-049b61514be7",
                "relationship--931f6b0d-5136-534a-93bc-8cce065e04dc",
                "attack-flow--b48ec5d9-407c-5e4a-a6d0-fe851cd4ea0e",
                "attack-pattern--f9e9365a-9ca2-4d9c-8e7c-050d73d1101a",
                "x-mitre-tactic--2558fd61-8c75-4730-94c4-11926db2a263",
                "attack-pattern--1a80d097-54df-41d8-9d33-34e755ec5e72",
                "x-mitre-tactic--5bc1d813-693e-4823-9961-abf9af4b0e92",
                "attack-action--c7e06b10-252d-520d-82eb-e32314bbec34",
            },
        ],
    ],
)
def test_parse_domain_flow(dummy_report, dummy_objects, dummy_flow, domain, expected_ids):
    tactics = get_all_tactics()
    techniques = get_techniques_from_extracted_objects(dummy_objects, tactics)
    flow = dummy_flow
    report = dummy_report
    flow_objects = parse_domain_flow(report, flow, techniques, tactics, domain)
    print([domain, {obj["id"] for obj in flow_objects}], ",")
    assert {obj["id"] for obj in flow_objects} == expected_ids


def test_get_techniques_from_extracted_objects(dummy_objects):
    tactics = get_all_tactics()
    techniques = get_techniques_from_extracted_objects(dummy_objects, tactics)
    stix_objects = [v.pop("stix_obj") for v in techniques.values()]
    assert dummy_objects == stix_objects
    assert techniques == {
        "T0814": {
            "domain": "ics-attack",
            "name": "Denial of Service",
            "possible_tactics": {"inhibit-response-function": "TA0107"},
            "id": "T0814",
            "platforms": [],
        },
        "T0887": {
            "domain": "ics-attack",
            "name": "Wireless Sniffing",
            "possible_tactics": {"discovery": "TA0102", "collection": "TA0100"},
            "id": "T0887",
            "platforms": [],
        },
        "T1505.001": {
            "domain": "enterprise-attack",
            "name": "SQL Stored Procedures",
            "possible_tactics": {"persistence": "TA0003"},
            "id": "T1505.001",
            "platforms": ["Windows", "Linux"],
        },
        "T1555.002": {
            "domain": "enterprise-attack",
            "name": "Securityd Memory",
            "possible_tactics": {"credential-access": "TA0006"},
            "id": "T1555.002",
            "platforms": ["Linux", "macOS"],
        },
    }


# def test_sjhsjh(dummy_report, dummy_objects):
#     ex = parse_model("openai:gpt-4o")
#     text = "The attck starts by sniffing with wireshark for packets with source 12155 after which a lot of SQLi requests is sent to the port causing a denial of service and then another method is used to bypass Securityd"

#     tactics = get_all_tactics()
#     techniques = get_techniques_from_extracted_objects(dummy_objects, tactics)

#     flow = ex.extract_attack_flow(text, techniques)

#     flow_objects = parse_flow(dummy_report, flow, techniques, tactics)


def test_extract_attack_flow_and_navigator(dummy_objects, dummy_report):
    bundler = MagicMock()
    bundler.report = dummy_report
    bundler.bundle.objects = dummy_objects
    ai_extractor = MagicMock()
    mock_extract_flow = ai_extractor.extract_attack_flow
    text = "My awesome text"

    tactics = get_all_tactics()
    techniques = get_techniques_from_extracted_objects(bundler.bundle.objects, tactics)

    with (
        patch("txt2stix.attack_flow.parse_flow") as mock_parse_flow,
        patch(
            "txt2stix.attack_flow.create_navigator_layer"
        ) as mock_create_navigator_layer,
    ):
        # ================= Both flow and navigator ===================
        flow, nav = extract_attack_flow_and_navigator(
            bundler, text, True, True, ai_extractor
        )
        assert bundler.flow_objects == mock_parse_flow.return_value
        assert (flow, nav) == (
            mock_extract_flow.return_value,
            mock_create_navigator_layer.return_value,
        )
        mock_parse_flow.assert_called_once_with(
            bundler.report, mock_extract_flow.return_value, techniques, tactics
        )
        mock_extract_flow.assert_called_once_with(text, techniques)

        mock_create_navigator_layer.assert_called_once_with(
            bundler.report,
            bundler.summary,
            mock_extract_flow.return_value,
            techniques,
            tactics,
        )

        ### reset mocks
        mock_parse_flow.reset_mock()
        mock_create_navigator_layer.reset_mock()
        mock_extract_flow.reset_mock()

        # ================= only flow ===================
        flow, nav = extract_attack_flow_and_navigator(
            bundler, text, True, False, ai_extractor
        )
        assert bundler.flow_objects == mock_parse_flow.return_value
        assert (flow, nav) == (mock_extract_flow.return_value, None)
        mock_parse_flow.assert_called_once_with(
            bundler.report, mock_extract_flow.return_value, techniques, tactics
        )
        mock_extract_flow.assert_called_once_with(text, techniques)

        mock_create_navigator_layer.assert_not_called()

        ### reset mocks
        mock_parse_flow.reset_mock()
        mock_create_navigator_layer.reset_mock()
        mock_extract_flow.reset_mock()

        # ================= only navigator ===================
        flow, nav = extract_attack_flow_and_navigator(
            bundler, text, False, True, ai_extractor
        )
        assert bundler.flow_objects == mock_parse_flow.return_value
        mock_extract_flow.assert_called_once_with(text, techniques)
        assert (flow, nav) == (
            mock_extract_flow.return_value,
            mock_create_navigator_layer.return_value,
        )
        mock_parse_flow.assert_not_called()

        mock_create_navigator_layer.assert_called_once_with(
            bundler.report,
            bundler.summary,
            mock_extract_flow.return_value,
            techniques,
            tactics,
        )

        ### reset mocks
        mock_parse_flow.reset_mock()
        mock_create_navigator_layer.reset_mock()
        mock_extract_flow.reset_mock()
        # ============ no technique object ============
        bundler.bundle.objects = []
        flow, nav = extract_attack_flow_and_navigator(
            bundler, text, True, True, ai_extractor
        )
        mock_extract_flow.assert_not_called()
        assert (flow, nav) == (None, None)
        mock_parse_flow.assert_not_called()

        mock_create_navigator_layer.assert_not_called()


def test_create_navigator_layer(dummy_report):
    summary = "this is a summary"
    flow = MagicMock()
    tactics_1 = {
        "TA01": "initial-access",
        "TA02": "lateral-movement",
        "TA03": "command-and-control",
    }
    tactics_2 = {
        "TA11": "initial-access",
        "TA12": "lateral-movement",
        "TA25": "command-and-control",
        "TA123": "persistence",
        "TA91": "exfiltration",
    }
    flow.items = [
        SimpleNamespace(
            attack_technique_id="T0001",
            attack_tactic_id="TA01",
            description="description 1",
        ),
        SimpleNamespace(
            attack_technique_id="T0003",
            attack_tactic_id="TA03",
            description="description 2",
        ),
        SimpleNamespace(
            attack_technique_id="T1001",
            attack_tactic_id="TA11",
            description="description 3",
        ),
        SimpleNamespace(
            attack_technique_id="T1002",
            attack_tactic_id="TA12",
            description="description 4",
        ),
        SimpleNamespace(
            attack_technique_id="T2001",
            attack_tactic_id="TA11",
            description="description 28jhsjhs",
        ),
        SimpleNamespace(
            attack_technique_id="T2003",
            attack_tactic_id="TA91",
            description="description sasa",
        ),
    ]
    techniques = {
        "T0001": dict(
            id="T0001", domain="enterprise-attack", possible_tactics=tactics_1
        ),
        "T0002": dict(
            id="T0002", domain="enterprise-attack", possible_tactics=tactics_1
        ),
        "T0003": dict(
            id="T0003", domain="enterprise-attack", possible_tactics=tactics_1
        ),
        "T1001": dict(id="T1001", domain="ics-attack", possible_tactics=tactics_2),
        "T1002": dict(id="T1002", domain="ics-attack", possible_tactics=tactics_2),
        "T1003": dict(id="T1003", domain="ics-attack", possible_tactics=tactics_2),
        "T2001": dict(id="T2001", domain="mobile-attack", possible_tactics=tactics_2),
        "T2002": dict(id="T2002", domain="mobile-attack", possible_tactics=tactics_2),
        "T2003": dict(id="T2003", domain="mobile-attack", possible_tactics=tactics_2),
    }

    retval = create_navigator_layer(
        dummy_report,
        summary,
        flow,
        techniques,
        tactics={
            "mobile-attack": {"version": "13.1"},
            "ics-attack": {"version": "17.0"},
            "enterprise-attack": {"version": "16.1"},
        },
    )
    assert len(retval) == 3
    assert retval == [
        {
            "versions": {
                "layer": "4.5",
                "attack": "16.1",
                "navigator": "5.1.0",
            },
            "name": "some markdown document",
            "domain": "enterprise-attack",
            "description": "this is a summary",
            "techniques": [],
            "gradient": {
                "colors": ["#ffffff", "#ff6666"],
                "minValue": 0,
                "maxValue": 100,
            },
            "legendItems": [],
            "metadata": [
                {
                    "name": "report_id",
                    "value": "report--9c88fbcb-8c0d-4124-868b-3dcb1e9b696c",
                }
            ],
            "links": [
                {
                    "label": "Generated using txt2stix",
                    "url": "https://github.com/muchdogesec/txt2stix/",
                }
            ],
            "layout": {"layout": "side"},
        },
        {
            "versions": {
                "layer": "4.5",
                "attack": "17.0",
                "navigator": "5.1.0",
            },
            "name": "some markdown document",
            "domain": "ics-attack",
            "description": "this is a summary",
            "techniques": [],
            "gradient": {
                "colors": ["#ffffff", "#ff6666"],
                "minValue": 0,
                "maxValue": 100,
            },
            "legendItems": [],
            "metadata": [
                {
                    "name": "report_id",
                    "value": "report--9c88fbcb-8c0d-4124-868b-3dcb1e9b696c",
                }
            ],
            "links": [
                {
                    "label": "Generated using txt2stix",
                    "url": "https://github.com/muchdogesec/txt2stix/",
                }
            ],
            "layout": {"layout": "side"},
        },
        {
            "versions": {
                "layer": "4.5",
                "attack": "13.1",
                "navigator": "5.1.0",
            },
            "name": "some markdown document",
            "domain": "mobile-attack",
            "description": "this is a summary",
            "techniques": [],
            "gradient": {
                "colors": ["#ffffff", "#ff6666"],
                "minValue": 0,
                "maxValue": 100,
            },
            "legendItems": [],
            "metadata": [
                {
                    "name": "report_id",
                    "value": "report--9c88fbcb-8c0d-4124-868b-3dcb1e9b696c",
                }
            ],
            "links": [
                {
                    "label": "Generated using txt2stix",
                    "url": "https://github.com/muchdogesec/txt2stix/",
                }
            ],
            "layout": {"layout": "side"},
        },
    ]


def test_create_navigator_layer__real_flow(dummy_report, dummy_flow, dummy_objects):
    tactics = get_all_tactics()
    techniques = get_techniques_from_extracted_objects(dummy_objects, tactics)
    retval = create_navigator_layer(
        dummy_report, "a summary", dummy_flow, techniques, tactics
    )
    assert len(retval) == 2
    assert retval == [
        {
            "versions": {
                "layer": "4.5",
                "attack": tactics["ics-attack"]["version"],
                "navigator": "5.1.0",
            },
            "name": "some markdown document",
            "domain": "ics-attack",
            "description": "a summary",
            "techniques": [
                {
                    "techniqueID": "T0814",
                    "tactic": "inhibit-response-function",
                    "score": 100,
                    "showSubtechniques": True,
                    "comment": "The SQL injection requests lead to a denial of service condition, disrupting the availability of the targeted service.",
                },
                {
                    "techniqueID": "T0887",
                    "tactic": "discovery",
                    "score": 100,
                    "showSubtechniques": True,
                    "comment": "The attack begins by using Wireshark to sniff network packets with a specific source, indicating a reconnaissance or discovery phase to gather information about the network traffic.",
                },
            ],
            "gradient": {
                "colors": ["#ffffff", "#ff6666"],
                "minValue": 0,
                "maxValue": 100,
            },
            "legendItems": [],
            "metadata": [
                {
                    "name": "report_id",
                    "value": "report--9c88fbcb-8c0d-4124-868b-3dcb1e9b696c",
                }
            ],
            "links": [
                {
                    "label": "Generated using txt2stix",
                    "url": "https://github.com/muchdogesec/txt2stix/",
                }
            ],
            "layout": {"layout": "side"},
        },
        {
            "versions": {
                "layer": "4.5",
                "attack": tactics["enterprise-attack"]["version"],
                "navigator": "5.1.0",
            },
            "name": "some markdown document",
            "domain": "enterprise-attack",
            "description": "a summary",
            "techniques": [
                {
                    "techniqueID": "T1505.001",
                    "tactic": "persistence",
                    "score": 100,
                    "showSubtechniques": True,
                    "comment": "A series of SQL injection requests are sent to a specific port, potentially to establish persistence or manipulate database operations.",
                },
                {
                    "techniqueID": "T1555.002",
                    "tactic": "credential-access",
                    "score": 100,
                    "showSubtechniques": True,
                    "comment": "An additional method is employed to bypass Securityd, likely to gain unauthorized access to credentials or sensitive information.",
                },
            ],
            "gradient": {
                "colors": ["#ffffff", "#ff6666"],
                "minValue": 0,
                "maxValue": 100,
            },
            "legendItems": [],
            "metadata": [
                {
                    "name": "report_id",
                    "value": "report--9c88fbcb-8c0d-4124-868b-3dcb1e9b696c",
                }
            ],
            "links": [
                {
                    "label": "Generated using txt2stix",
                    "url": "https://github.com/muchdogesec/txt2stix/",
                }
            ],
            "layout": {"layout": "side"},
        },
    ]


@pytest.fixture
def dummy_objects():
    return [
        # 2 ics objects
        {
            "created": "2020-05-21T17:43:26.506Z",
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "description": "Adversaries may perform Denial-of-Service (DoS) attacks to disrupt expected device functionality. Examples of DoS attacks include overwhelming the target device with a high volume of requests in a short time period and sending the target device a request it does not know how to handle. Disrupting device state may temporarily render it unresponsive, possibly lasting until a reboot can occur. When placed in this state, devices may be unable to send and receive requests, and may not perform expected response functions in reaction to other events in the environment. \n\nSome ICS devices are particularly sensitive to DoS events, and may become unresponsive in reaction to even a simple ping sweep. Adversaries may also attempt to execute a Permanent Denial-of-Service (PDoS) against certain devices, such as in the case of the BrickerBot malware. (Citation: ICS-CERT April 2017) \n\nAdversaries may exploit a software vulnerability to cause a denial of service by taking advantage of a programming error in a program, service, or within the operating system software or kernel itself to execute adversary-controlled code. Vulnerabilities may exist in software that can be used to cause a denial of service condition. \n\nAdversaries may have prior knowledge about industrial protocols or control devices used in the environment through [Remote System Information Discovery](https://attack.mitre.org/techniques/T0888). There are examples of adversaries remotely causing a [Device Restart/Shutdown](https://attack.mitre.org/techniques/T0816) by exploiting a vulnerability that induces uncontrolled resource consumption. (Citation: ICS-CERT August 2018) (Citation: Common Weakness Enumeration January 2019) (Citation: MITRE March 2018) ",
            "external_references": [
                {
                    "source_name": "mitre-attack",
                    "url": "https://attack.mitre.org/techniques/T0814",
                    "external_id": "T0814",
                },
                {
                    "source_name": "Common Weakness Enumeration January 2019",
                    "description": "Common Weakness Enumeration 2019, January 03 CWE-400: Uncontrolled Resource Consumption Retrieved. 2019/03/14 ",
                    "url": "http://cwe.mitre.org/data/definitions/400.html",
                },
                {
                    "source_name": "ICS-CERT April 2017",
                    "description": "ICS-CERT 2017, April 18 CS Alert (ICS-ALERT-17-102-01A) BrickerBot Permanent Denial-of-Service Attack Retrieved. 2019/10/24 ",
                    "url": "https://www.us-cert.gov/ics/alerts/ICS-ALERT-17-102-01A",
                },
                {
                    "source_name": "ICS-CERT August 2018",
                    "description": "ICS-CERT 2018, August 27 Advisory (ICSA-15-202-01) - Siemens SIPROTEC Denial-of-Service Vulnerability Retrieved. 2019/03/14 ",
                    "url": "https://ics-cert.us-cert.gov/advisories/ICSA-15-202-01",
                },
                {
                    "source_name": "MITRE March 2018",
                    "description": "MITRE 2018, March 22 CVE-2015-5374 Retrieved. 2019/03/14 ",
                    "url": "https://nvd.nist.gov/vuln/detail/CVE-2015-5374",
                },
            ],
            "id": "attack-pattern--1b22b676-9347-4c55-9a35-ef0dc653db5b",
            "kill_chain_phases": [
                {
                    "kill_chain_name": "mitre-ics-attack",
                    "phase_name": "inhibit-response-function",
                }
            ],
            "modified": "2024-10-14T19:00:55.006Z",
            "name": "Denial of Service",
            "object_marking_refs": [
                "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
            ],
            "revoked": False,
            "spec_version": "2.1",
            "type": "attack-pattern",
            "x_mitre_attack_spec_version": "3.2.0",
            "x_mitre_data_sources": [
                "Network Traffic: Network Traffic Content",
                "Network Traffic: Network Traffic Flow",
                "Application Log: Application Log Content",
                "Operational Databases: Process History/Live Data",
            ],
            "x_mitre_deprecated": False,
            "x_mitre_detection": "",
            "x_mitre_domains": ["ics-attack"],
            "x_mitre_is_subtechnique": False,
            "x_mitre_modified_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "x_mitre_platforms": ["None"],
            "x_mitre_version": "1.1",
        },
        {
            "created": "2020-05-21T17:43:26.506Z",
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "description": "Adversaries may seek to capture radio frequency (RF) communication used for remote control and reporting in distributed environments. RF communication frequencies vary between 3 kHz to 300 GHz, although are commonly between 300 MHz to 6 GHz. (Citation: Candell, R., Hany, M., Lee, K. B., Liu,Y., Quimby, J., Remley, K. April 2018)  The wavelength and frequency of the signal affect how the signal propagates through open air, obstacles (e.g. walls and trees) and the type of radio required to capture them. These characteristics are often standardized in the protocol and hardware and may have an effect on how the signal is captured. Some examples of wireless protocols that may be found in cyber-physical environments are: WirelessHART, Zigbee, WIA-FA, and 700 MHz Public Safety Spectrum. \n\nAdversaries may capture RF communications by using specialized hardware, such as software defined radio (SDR), handheld radio, or a computer with radio demodulator tuned to the communication frequency. (Citation: Bastille April 2017) Information transmitted over a wireless medium may be captured in-transit whether the sniffing device is the intended destination or not. This technique may be particularly useful to an adversary when the communications are not encrypted. (Citation: Gallagher, S. April 2017) \n\nIn the 2017 Dallas Siren incident, it is suspected that adversaries likely captured wireless command message broadcasts on a 700 MHz frequency during a regular test of the system. These messages were later replayed to trigger the alarm systems. (Citation: Gallagher, S. April 2017)",
            "external_references": [
                {
                    "source_name": "mitre-attack",
                    "url": "https://attack.mitre.org/techniques/T0887",
                    "external_id": "T0887",
                },
                {
                    "source_name": "Bastille April 2017",
                    "description": "Bastille 2017, April 17 Dallas Siren Attack Retrieved. 2020/11/06 ",
                    "url": "https://www.bastille.net/blogs/2017/4/17/dallas-siren-attack",
                },
                {
                    "source_name": "Candell, R., Hany, M., Lee, K. B., Liu,Y., Quimby, J., Remley, K. April 2018",
                    "description": "Candell, R., Hany, M., Lee, K. B., Liu,Y., Quimby, J., Remley, K. 2018, April Guide to Industrial Wireless Systems Deployments Retrieved. 2020/12/01 ",
                    "url": "https://nvlpubs.nist.gov/nistpubs/ams/NIST.AMS.300-4.pdf",
                },
                {
                    "source_name": "Gallagher, S. April 2017",
                    "description": "Gallagher, S. 2017, April 12 Pirate radio: Signal spoof set off Dallas emergency sirens, not network hack Retrieved. 2020/12/01 ",
                    "url": "https://arstechnica.com/information-technology/2017/04/dallas-siren-hack-used-radio-signals-to-spoof-alarm-says-city-manager/",
                },
            ],
            "id": "attack-pattern--0fe075d5-beac-4d02-b93e-0f874997db72",
            "kill_chain_phases": [
                {"kill_chain_name": "mitre-ics-attack", "phase_name": "discovery"},
                {"kill_chain_name": "mitre-ics-attack", "phase_name": "collection"},
            ],
            "modified": "2023-10-13T17:56:59.193Z",
            "name": "Wireless Sniffing",
            "object_marking_refs": [
                "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
            ],
            "revoked": False,
            "spec_version": "2.1",
            "type": "attack-pattern",
            "x_mitre_attack_spec_version": "2.1.0",
            "x_mitre_contributors": ["ICSCoE Japan"],
            "x_mitre_data_sources": ["Network Traffic: Network Traffic Flow"],
            "x_mitre_deprecated": False,
            "x_mitre_detection": "",
            "x_mitre_domains": ["ics-attack"],
            "x_mitre_is_subtechnique": False,
            "x_mitre_modified_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "x_mitre_platforms": ["None"],
            "x_mitre_version": "1.1",
        },
        # 1 enterprise object
        {
            "created": "2019-12-12T14:59:58.168Z",
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "description": "Adversaries may abuse SQL stored procedures to establish persistent access to systems. SQL Stored Procedures are code that can be saved and reused so that database users do not waste time rewriting frequently used SQL queries. Stored procedures can be invoked via SQL statements to the database using the procedure name or via defined events (e.g. when a SQL server application is started/restarted).\n\nAdversaries may craft malicious stored procedures that can provide a persistence mechanism in SQL database servers.(Citation: NetSPI Startup Stored Procedures)(Citation: Kaspersky MSSQL Aug 2019) To execute operating system commands through SQL syntax the adversary may have to enable additional functionality, such as xp_cmdshell for MSSQL Server.(Citation: NetSPI Startup Stored Procedures)(Citation: Kaspersky MSSQL Aug 2019)(Citation: Microsoft xp_cmdshell 2017) \n\nMicrosoft SQL Server can enable common language runtime (CLR) integration. With CLR integration enabled, application developers can write stored procedures using any .NET framework language (e.g. VB .NET, C#, etc.).(Citation: Microsoft CLR Integration 2017) Adversaries may craft or modify CLR assemblies that are linked to stored procedures since these CLR assemblies can be made to execute arbitrary commands.(Citation: NetSPI SQL Server CLR) ",
            "external_references": [
                {
                    "source_name": "mitre-attack",
                    "url": "https://attack.mitre.org/techniques/T1505/001",
                    "external_id": "T1505.001",
                },
                {
                    "source_name": "Microsoft CLR Integration 2017",
                    "description": "Microsoft. (2017, June 19). Common Language Runtime Integration. Retrieved July 8, 2019.",
                    "url": "https://docs.microsoft.com/en-us/sql/relational-databases/clr-integration/common-language-runtime-integration-overview?view=sql-server-2017",
                },
                {
                    "source_name": "Microsoft xp_cmdshell 2017",
                    "description": "Microsoft. (2017, March 15). xp_cmdshell (Transact-SQL). Retrieved September 9, 2019.",
                    "url": "https://docs.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/xp-cmdshell-transact-sql?view=sql-server-2017",
                },
                {
                    "source_name": "Kaspersky MSSQL Aug 2019",
                    "description": "Plakhov, A., Sitchikhin, D. (2019, August 22). Agent 1433: remote attack on Microsoft SQL Server. Retrieved September 4, 2019.",
                    "url": "https://securelist.com/malicious-tasks-in-ms-sql-server/92167/",
                },
                {
                    "source_name": "NetSPI Startup Stored Procedures",
                    "description": "Sutherland, S. (2016, March 7). Maintaining Persistence via SQL Server – Part 1: Startup Stored Procedures. Retrieved September 12, 2024.",
                    "url": "https://www.netspi.com/blog/technical-blog/network-penetration-testing/sql-server-persistence-part-1-startup-stored-procedures/",
                },
                {
                    "source_name": "NetSPI SQL Server CLR",
                    "description": "Sutherland, S. (2017, July 13). Attacking SQL Server CLR Assemblies. Retrieved September 12, 2024.",
                    "url": "https://www.netspi.com/blog/technical-blog/adversary-simulation/attacking-sql-server-clr-assemblies/",
                },
            ],
            "id": "attack-pattern--f9e9365a-9ca2-4d9c-8e7c-050d73d1101a",
            "kill_chain_phases": [
                {"kill_chain_name": "mitre-attack", "phase_name": "persistence"}
            ],
            "modified": "2024-10-15T16:05:24.007Z",
            "name": "SQL Stored Procedures",
            "object_marking_refs": [
                "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
            ],
            "revoked": False,
            "spec_version": "2.1",
            "type": "attack-pattern",
            "x_mitre_attack_spec_version": "3.2.0",
            "x_mitre_contributors": [
                "Carlos Borges, @huntingneo, CIP",
                "Lucas da Silva Pereira, @vulcanunsec, CIP",
                "Kaspersky",
            ],
            "x_mitre_data_sources": ["Application Log: Application Log Content"],
            "x_mitre_deprecated": False,
            "x_mitre_detection": "On a MSSQL Server, consider monitoring for xp_cmdshell usage.(Citation: NetSPI Startup Stored Procedures) Consider enabling audit features that can log malicious startup activities.",
            "x_mitre_domains": ["enterprise-attack"],
            "x_mitre_is_subtechnique": True,
            "x_mitre_modified_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "x_mitre_platforms": ["Windows", "Linux"],
            "x_mitre_version": "1.1",
        },
        # 1 mobile object
        {
            "created": "2020-02-12T18:56:31.051Z",
            "created_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "description": "An adversary with root access may gather credentials by reading `securityd`’s memory. `securityd` is a service/daemon responsible for implementing security protocols such as encryption and authorization.(Citation: Apple Dev SecurityD) A privileged adversary may be able to scan through `securityd`'s memory to find the correct sequence of keys to decrypt the user’s logon keychain. This may provide the adversary with various plaintext passwords, such as those for users, WiFi, mail, browsers, certificates, secure notes, etc.(Citation: OS X Keychain)(Citation: OSX Keydnap malware)\n\nIn OS X prior to El Capitan, users with root access can read plaintext keychain passwords of logged-in users because Apple’s keychain implementation allows these credentials to be cached so that users are not repeatedly prompted for passwords.(Citation: OS X Keychain)(Citation: External to DA, the OS X Way) Apple’s `securityd` utility takes the user’s logon password, encrypts it with PBKDF2, and stores this master key in memory. Apple also uses a set of keys and algorithms to encrypt the user’s password, but once the master key is found, an adversary need only iterate over the other values to unlock the final password.(Citation: OS X Keychain)",
            "external_references": [
                {
                    "source_name": "mitre-attack",
                    "url": "https://attack.mitre.org/techniques/T1555/002",
                    "external_id": "T1555.002",
                },
                {
                    "source_name": "External to DA, the OS X Way",
                    "description": "Alex Rymdeko-Harvey, Steve Borosh. (2016, May 14). External to DA, the OS X Way. Retrieved September 12, 2024.",
                    "url": "https://www.slideshare.net/slideshow/external-to-da-the-os-x-way/62021418",
                },
                {
                    "source_name": "Apple Dev SecurityD",
                    "description": "Apple. (n.d.). Security Server and Security Agent. Retrieved March 29, 2024.",
                    "url": "https://developer.apple.com/library/archive/documentation/Security/Conceptual/Security_Overview/Architecture/Architecture.html",
                },
                {
                    "source_name": "OS X Keychain",
                    "description": "Juuso Salonen. (2012, September 5). Breaking into the OS X keychain. Retrieved July 15, 2017.",
                    "url": "http://juusosalonen.com/post/30923743427/breaking-into-the-os-x-keychain",
                },
                {
                    "source_name": "OSX Keydnap malware",
                    "description": "Marc-Etienne M.Leveille. (2016, July 6). New OSX/Keydnap malware is hungry for credentials. Retrieved July 3, 2017.",
                    "url": "https://www.welivesecurity.com/2016/07/06/new-osxkeydnap-malware-hungry-credentials/",
                },
            ],
            "id": "attack-pattern--1a80d097-54df-41d8-9d33-34e755ec5e72",
            "kill_chain_phases": [
                {"kill_chain_name": "mitre-attack", "phase_name": "credential-access"}
            ],
            "modified": "2024-10-15T16:41:18.638Z",
            "name": "Securityd Memory",
            "object_marking_refs": [
                "marking-definition--fa42a846-8d90-4e51-bc29-71d5b4802168"
            ],
            "revoked": False,
            "spec_version": "2.1",
            "type": "attack-pattern",
            "x_mitre_attack_spec_version": "3.2.0",
            "x_mitre_data_sources": [
                "Command: Command Execution",
                "Process: Process Access",
            ],
            "x_mitre_deprecated": False,
            "x_mitre_detection": "Monitor processes and command-line arguments for activity surrounded users searching for credentials or using automated tools to scan memory for passwords.",
            "x_mitre_domains": ["enterprise-attack"],
            "x_mitre_is_subtechnique": True,
            "x_mitre_modified_by_ref": "identity--c78cb6e5-0c4b-4611-8297-d1b8b55e40b5",
            "x_mitre_platforms": ["Linux", "macOS"],
            "x_mitre_version": "1.2",
        },
    ]


@pytest.fixture
def dummy_report():
    return Report(
        **{
            "confidence": 0,
            "created": "2025-03-10T15:06:31.567505Z",
            "created_by_ref": "identity--e92c648d-03eb-59a5-a318-9a36e6f8057c",
            "description": "[comment]:<> (===START PAGE 1===)\n\n### My threat intel report\n\n**fakedomain.com**\nresolves to 1.1.1.1.\n[fakedomain.com](https://fakedomain.com)\n*has been known*\nto distribute revil malware sent in email attachments from the email address\n[fakedomain@email.com](mailto:fakedomain@email.com)\n\n![](0_image_0.png)\n\n\n\n[comment]:<> (===END PAGE 1===)\n",
            "external_references": [
                {
                    "source_name": "txt2stix_report_id",
                    "external_id": "9c88fbcb-8c0d-4124-868b-3dcb1e9b696c",
                },
                {
                    "source_name": "txt2stix Report MD5",
                    "description": "d7902d427a24667c3ace51e00c637589",
                },
                {
                    "source_name": "stixify_profile_id",
                    "external_id": "64ca67f0-753a-51b5-a64b-de73184c5457",
                },
            ],
            "id": "report--9c88fbcb-8c0d-4124-868b-3dcb1e9b696c",
            "modified": "2025-03-10T15:06:34.423062Z",
            "name": "some markdown document",
            "object_marking_refs": [
                "marking-definition--e828b379-4e03-4974-9ac4-e53a884c97c1",
                "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5",
            ],
            "object_refs": [attack_flow_ExtensionDefinitionSMO.id],
            "published": "2025-03-10T15:06:34.423036Z",
            "spec_version": "2.1",
            "type": "report",
        },
    )


@pytest.fixture
def dummy_flow():
    return AttackFlowList.model_validate(
        {
            "items": [
                {
                    "position": 0,
                    "attack_technique_id": "T0887",
                    "name": "Packet Sniffing with Wireshark",
                    "description": "The attack begins by using Wireshark to sniff network packets with a specific source, indicating a reconnaissance or discovery phase to gather information about the network traffic.",
                },
                {
                    "position": 1,
                    "attack_technique_id": "T1505.001",
                    "name": "SQL Injection for Persistence",
                    "description": "A series of SQL injection requests are sent to a specific port, potentially to establish persistence or manipulate database operations.",
                },
                {
                    "position": 2,
                    "attack_technique_id": "T0814",
                    "name": "Denial of Service via SQLi",
                    "description": "The SQL injection requests lead to a denial of service condition, disrupting the availability of the targeted service.",
                },
                {
                    "position": 3,
                    "attack_technique_id": "T1555.002",
                    "name": "Bypassing Securityd",
                    "description": "An additional method is employed to bypass Securityd, likely to gain unauthorized access to credentials or sensitive information.",
                },
            ],
            "success": True,
            "tactic_selection": [
                ("T0887", "discovery"),
                ("T1505.001", "persistence"),
                ("T0814", "inhibit-response-function"),
                ("T1555.002", "credential-access"),
            ],
        }
    )
