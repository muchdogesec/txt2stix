from datetime import datetime
import pytest
from unittest import mock
from unittest.mock import MagicMock
from pathlib import Path
import sys
import os
from stix2extensions._extensions import attack_flow_ExtensionDefinitionSMO

from txt2stix import get_all_extractors
from txt2stix.ai_extractor.utils import (
    AttackFlowItem,
    AttackFlowList,
    DescribesIncident,
)
from txt2stix.attack_flow import parse_flow
from txt2stix.stix import txt2stixBundler
from txt2stix.txt2stix import (
    parse_args,
    parse_extractors_globbed,
    parse_model,
    run_txt2stix,
    split_comma,
    range_type,
    parse_labels,
    load_env,
    # run_txt2stix,
    extract_all,
    extract_relationships_with_ai,
)
from stix2 import Report
from txt2stix.common import FatalException
import argparse


def get_flow_items(items):
    retval = []
    for pos, (tactic_id, tecnique_id) in enumerate(items):
        retval.append(
            AttackFlowItem(
                position=pos,
                attack_tactic_id=tactic_id,
                attack_technique_id=tecnique_id,
                name=f"{tactic_id}+{tecnique_id}",
                description=f"Tactic ID is {tactic_id} and Technique ID is {tecnique_id}",
            )
        )
    return retval


@pytest.mark.parametrize(
    ["flow", "expected_ids"],
    [
        [
            AttackFlowList(
                success=True,
                matrix="enterprise",
                items=get_flow_items([("TA0009", "T1653"), ("TA0040", "T1027")]),
            ),
            [
                "relationship--6346ead9-49cc-5ede-89e2-449f1c22ed13",
                "attack-action--a3920f17-1d1f-5ace-982f-235a65d53611",
                "x-mitre-tactic--5569339b-94c2-49ee-afb3-2222936582c8",
                "attack-action--34ae999a-5eaa-568b-a584-863080211b14",
                "attack-pattern--ea071aa0-8f17-416f-ab0d-2bab7e79003d",
                "x-mitre-tactic--d108ce10-2419-4cf9-a774-46161d6c6cfe",
                "attack-pattern--b3d682b6-98f2-4fb0-aa3b-b4df007ca70a",
                "attack-flow--9c88fbcb-8c0d-4124-868b-3dcb1e9b696c",
            ],
        ],
        [
            AttackFlowList(
                success=False,
                matrix="enterprise",
                items=get_flow_items([("TA0009", "T1653"), ("TA0040", "T1027")]),
            ),
            [
            ],
        ],
        
    ],
)
def test_parse_flow(flow: AttackFlowList, expected_ids):
    report = Report(
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
    expected_ids = set(expected_ids)
    expected_ids.add(report.id)
    expected_ids.add(attack_flow_ExtensionDefinitionSMO.id)

    flow_objects = parse_flow(report, flow)
    if not flow.success:
        assert len(flow_objects) == 0
        return
    assert expected_ids == {obj["id"] for obj in flow_objects}


# test_parse_flow(
#     AttackFlowList(
#         success=True,
#         matrix="enterprise",
#         items=get_flow_items([("TA0009", "T1653"), ("TA0040", "T1027")]),
#     ),
#     [],
# )
