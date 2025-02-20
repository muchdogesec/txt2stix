import logging
import uuid
from stix2 import Relationship

from txt2stix.retriever import STIXObjectRetriever
from stix2extensions.attack_action import AttackAction, AttackFlow
from stix2extensions._extensions import attack_flow_ExtensionDefinitionSMO
from .utils import AttackFlowList

def parse_flow(report, flow: AttackFlowList):
    logging.info(f"flow.success = {flow.success}")
    if not flow.success:
        return []
    attack_objects = STIXObjectRetriever().get_attack_objects(
        flow.matrix,
        [item.attack_tactic_id for item in flow.items]
        + [item.attack_technique_id for item in flow.items],
    )
    attack_objects = {
        obj["external_references"][0]["external_id"]: obj for obj in attack_objects
    }
    flow_objects = [report, attack_flow_ExtensionDefinitionSMO]
    last_action = None
    for i, item in enumerate(flow.items):
        try:
            tactic_obj = attack_objects[item.attack_tactic_id]
            technique_obj = attack_objects[item.attack_technique_id]
            action_obj = AttackAction(
                **{
                    "id": f"attack-action--{str(uuid.uuid4())}",
                    "effect_refs": [f"attack-action--{str(uuid.uuid4())}"],
                    "technique_id": item.attack_technique_id,
                    "technique_ref": technique_obj["id"],
                    "tactic_id": item.attack_tactic_id,
                    "tactic_ref": tactic_obj["id"],
                    "name": item.name,
                    "description": item.description,
                },
                allow_custom=True,
            )
            action_obj.effect_refs.clear()
            if i == 0:
                flow_obj = {
                    "type": "attack-flow",
                    "id": report.id.replace("report", "attack-flow"),
                    "spec_version": "2.1",
                    "created": report.created,
                    "modified": report.modified,
                    "created_by_ref": report.created_by_ref,
                    "start_refs": [action_obj["id"]],
                    "name": report.name,
                    "description": report.description,
                    "scope": "malware",
                    "external_references": report.external_references,
                    "object_marking_refs": report.object_marking_refs,
                }
                flow_objects.append(AttackFlow(**flow_obj))
                flow_objects.append(
                    Relationship(
                        type="relationship",
                        spec_version="2.1",
                        # id="relationship--<UUID V5>",
                        created_by_ref=report.created_by_ref,
                        created=report.created,
                        modified=report.modified,
                        relationship_type="attack-flow",
                        description=f"Attack Flow for {report.name}",
                        source_ref=report.id,
                        target_ref=flow_obj['id'],
                        external_references=report.external_references,
                        object_marking_refs=report.object_marking_refs,
                    )
                )
            else:
                last_action["effect_refs"].append(action_obj["id"])
            flow_objects.append(tactic_obj)
            flow_objects.append(technique_obj)
            flow_objects.append(action_obj)
            last_action = action_obj
        except:
            if flow_objects == 0:
                logging.exception("FATAL: create attack flow object failed")
                return []
            logging.debug("create attack-action failed", exc_info=True)

    return flow_objects
