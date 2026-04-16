import json
import logging
import uuid
from stix2 import Relationship
from txt2stix import txt2stixBundler

from txt2stix.ai_extractor.base import BaseAIExtractor
from txt2stix.common import UUID_NAMESPACE
from txt2stix.retriever import STIXObjectRetriever
from stix2extensions import AttackAction, AttackFlow, Procedure
from .utils import AttackFlowList


def parse_flow(report, flow: AttackFlowList, techniques, tactics):
    logging.info(f"flow.success = {flow.success}")
    if not flow.success:
        return []
    objects = [report]
    for domain in ["enterprise-attack", "mobile-attack", "ics-attack"]:
        flow_objects = parse_domain_flow(report, flow, techniques, tactics, domain)
        objects.extend(flow_objects)
    return objects


def parse_domain_flow(report, flow: AttackFlowList, techniques, tactics, domain):
    flow_objects = []
    flow_obj = None
    last_action = None
    for i, item in enumerate(flow.items):
        try:
            technique = techniques[item.attack_technique_id]
            if technique["domain"] != domain:
                continue
            tactic_id = technique["possible_tactics"][
                flow.tactic_mapping[item.attack_technique_id]
            ]
            technique_obj = technique["stix_obj"]

            tactic_obj = tactics[technique["domain"]][tactic_id]
            action_obj = AttackAction(
                **{
                    "id": flow_id(report["id"], item.attack_technique_id, tactic_id),
                    "effect_refs": [f"attack-action--{str(uuid.uuid4())}"],
                    "technique_id": item.attack_technique_id,
                    "technique_ref": technique_obj["id"],
                    "tactic_id": tactic_id,
                    "tactic_ref": tactic_obj["id"],
                    "name": item.name,
                    "description": item.description,
                },
                allow_custom=True,
            )
            action_obj.effect_refs.clear()
            if not flow_obj:
                flow_obj = {
                    "type": "attack-flow",
                    "id": "attack-flow--"
                    + str(
                        uuid.uuid5(
                            UUID_NAMESPACE, f"attack-flow+{domain}+{report['id']}"
                        )
                    ),
                    "spec_version": "2.1",
                    "created": report["created"],
                    "modified": report["modified"],
                    "created_by_ref": report["created_by_ref"],
                    "start_refs": [action_obj["id"]],
                    "name": f"[{domain.split('-')[0].upper()}] {report['name']}",
                    "description": report["description"],
                    "scope": "malware",
                    "external_references": report["external_references"],
                    "object_marking_refs": report["object_marking_refs"],
                }
                flow_objects.append(AttackFlow(**flow_obj))
                flow_objects.append(
                    Relationship(
                        type="relationship",
                        spec_version="2.1",
                        id="relationship--"
                        + str(
                            uuid.uuid5(
                                UUID_NAMESPACE,
                                f"attack-flow+{report['id']}+{flow_obj['id']}",
                            )
                        ),
                        created_by_ref=report["created_by_ref"],
                        created=report["created"],
                        modified=report["modified"],
                        relationship_type="attack-flow",
                        description=f"Attack Flow for {report['name']}",
                        source_ref=report["id"],
                        target_ref=flow_obj["id"],
                        external_references=report["external_references"],
                        object_marking_refs=report["object_marking_refs"],
                    )
                )
            else:
                last_action["effect_refs"].append(action_obj["id"])
            flow_objects.append(tactic_obj)
            flow_objects.append(technique_obj)
            flow_objects.append(action_obj)
            last_action = action_obj
        except Exception as e:
            if flow_objects == 2:
                logging.exception("FATAL: create attack flow object failed")
                return []
            logging.debug("create attack-action failed", exc_info=True)
            raise

    return flow_objects


def flow_id(report_id, technique_id, tactic_id):
    return "attack-action--" + str(
        uuid.uuid5(
            uuid.UUID(report_id.split("--")[-1]),
            f"{report_id}+{technique_id}+{tactic_id}",
        )
    )


def get_all_tactics():
    tactics = {
        "enterprise-attack": None,
        "mobile-attack": None,
        "ics-attack": None,
    }
    for k in tactics.keys():
        matrix = k.replace("attack", "").strip("-")
        all_tactics = STIXObjectRetriever().get_attack_tactics(matrix)
        tactics[k] = all_tactics
    return tactics


def get_techniques_from_extracted_objects(objects: dict, tactics: dict):
    techniques = {}
    for obj in objects:
        if (
            obj["type"] == "attack-pattern"
            and obj.get("external_references", [{"source_name": None}])[0][
                "source_name"
            ]
            == "mitre-attack"
        ):
            domain = obj["x_mitre_domains"][0]
            technique = dict(
                domain=domain,
                name=obj["name"],
                possible_tactics={},
                id=obj["external_references"][0]["external_id"],
                platforms=[
                    platform
                    for platform in obj["x_mitre_platforms"]
                    if platform != "None"
                ],
                stix_obj=obj,
            )
            for phase in obj["kill_chain_phases"]:
                if not set(phase["kill_chain_name"].split("-")).issuperset(
                    ["mitre", "attack"]
                ):
                    continue
                tactic_name = phase["phase_name"]
                tactic_obj = tactics[domain][tactic_name]
                tactic_id = tactic_obj["external_references"][0]["external_id"]
                technique["possible_tactics"][tactic_name] = tactic_id
            techniques[technique["id"]] = technique
    return techniques


def create_navigator_layer(report, summary, flow: AttackFlowList, techniques, tactics):
    domains = {}
    comments = {item.attack_technique_id: item.description for item in flow.items}
    for technique in techniques.values():
        domain_techniques = domains.setdefault(technique["domain"], [])
        technique_id = technique["id"]
        if technique_id not in flow.tactic_mapping:
            continue
        technique_item = dict(
            techniqueID=technique_id,
            tactic=flow.tactic_mapping[technique_id],
            score=100,
            showSubtechniques=True,
        )
        if comment := comments.get(technique_id):
            technique_item["comment"] = comment
        domain_techniques.append(technique_item)

    retval = []

    for domain, domain_techniques in domains.items():
        retval.append(
            {
                "versions": {
                    "layer": "4.5",
                    "attack": tactics[domain]["version"],
                    "navigator": "5.1.0",
                },
                "name": report["name"],
                "domain": domain,
                "description": summary,
                "techniques": domain_techniques,
                "gradient": {
                    "colors": ["#ffffff", "#ff6666"],
                    "minValue": 0,
                    "maxValue": 100,
                },
                "legendItems": [],
                "metadata": [{"name": "report_id", "value": report["id"]}],
                "links": [
                    {
                        "label": "Generated using txt2stix",
                        "url": "https://github.com/muchdogesec/txt2stix/",
                    }
                ],
                "layout": {"layout": "side"},
            }
        )
    return retval


def extract_attack_flow_and_navigator(
    bundler: txt2stixBundler,
    preprocessed_text,
    ai_create_attack_flow,
    ai_create_attack_navigator_layer,
    ai_settings_relationships,
    flow=None,
):
    ex: BaseAIExtractor = ai_settings_relationships
    tactics = get_all_tactics()
    techniques = get_techniques_from_extracted_objects(bundler.bundle.objects, tactics)
    if not techniques:
        return None, None

    logged_techniques = [
        {k: v for k, v in t.items() if k != "stix_obj"} for t in techniques.values()
    ]
    logging.debug(f"parsed techniques: {json.dumps(logged_techniques, indent=4)}")

    flow = flow or ex.extract_attack_flow(preprocessed_text, techniques)
    navigator = None
    if ai_create_attack_flow:
        logging.info("creating attack-flow bundle")
        bundler.flow_objects = parse_flow(bundler.report, flow, techniques, tactics)
        for obj in make_procedures_from_flow(
            flow, bundler.report, techniques, bundler.flow_objects
        ):
            bundler.add_ref(obj, is_report_object=True)

    if ai_create_attack_navigator_layer:
        navigator = create_navigator_layer(
            bundler.report, bundler.summary, flow, techniques, tactics
        )
    return flow, navigator


def make_procedures_from_flow(
    flow: AttackFlowList, report, techniques, flow_objects
) -> list[Procedure]:
    """Create STIX Procedure objects from attack flow items.

    Args:
        flow: AttackFlowList containing the attack flow items
        report: Report object for created and modified timestamps and created_by_ref

    Returns:
        List of Procedure STIX objects
    """
    retval = []
    flow_objects_by_technique_id = {
        obj["technique_id"]: obj
        for obj in flow_objects
        if obj["type"] == "attack-action"
    }
    for item in flow.items:
        # Generate deterministic ID based on technique, name, and report (if provided)
        id_base = f"{report['id']}+{item.name}"
        procedure_id = f"procedure--{str(uuid.uuid5(UUID_NAMESPACE, id_base))}"
        technique = techniques[item.attack_technique_id]["stix_obj"]
        # Create Procedure object
        procedure = Procedure(
            id=procedure_id,
            name=item.name,
            created=report["created"],
            modified=report["modified"],
            created_by_ref=report["created_by_ref"],
            object_marking_refs=report["object_marking_refs"],
            description=item.description,
            context=item.context,
            objective=item.objective,
            variants=item.variants,
            external_references=[
                dict(
                    source_name="txt2stix_report_id",
                    external_id=report["id"],
                ),
                technique["external_references"][0],
            ],
        )
        retval.append(procedure)
        retval.append(
            Relationship(
                type="relationship",
                spec_version="2.1",
                id="relationship--"
                + str(
                    uuid.uuid5(
                        UUID_NAMESPACE, f"procedure+{procedure.id}+{technique['id']}"
                    )
                ),
                created_by_ref=procedure.created_by_ref,
                created=procedure.created,
                modified=procedure.modified,
                relationship_type="related-to",
                description=f"{procedure.name} is related to {technique['name']}",
                source_ref=procedure.id,
                target_ref=technique["id"],
                external_references=procedure.external_references,
                object_marking_refs=procedure.object_marking_refs,
            )
        )

        flow_obj = flow_objects_by_technique_id.get(item.attack_technique_id)
        if flow_obj:
            retval.append(
                Relationship(
                    type="relationship",
                    spec_version="2.1",
                    id="relationship--"
                    + str(
                        uuid.uuid5(
                            UUID_NAMESPACE, f"procedure+{procedure.id}+{flow_obj['id']}"
                        )
                    ),
                    created_by_ref=procedure.created_by_ref,
                    created=procedure.created,
                    modified=procedure.modified,
                    relationship_type="related-to",
                    description=procedure.name,
                    source_ref=procedure.id,
                    target_ref=flow_obj["id"],
                    external_references=procedure.external_references,
                    object_marking_refs=procedure.object_marking_refs,
                )
            )

    return retval
