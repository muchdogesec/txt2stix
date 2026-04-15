import logging
from stix2 import (
    Identity,
    MarkingDefinition,
    Bundle,
)
from stix2.parsing import dict_to_stix2, parse as parse_stix
from stix2.serialization import serialize
from stix2validator.v21.shoulds import relationships_strict
import hashlib
from stix2 import (
    v21,
)
import requests


from .common import UUID_NAMESPACE, MinorException, TXT2STIX_IDENTITY, TXT2STIX_MARKING
from datetime import UTC, datetime as dt
import uuid
import json
from .indicator import build_observables
from .tlp_levels import TLP_LEVEL


logger = logging.getLogger("txt2stix.stix")

class txt2stixBundler:
    EXTENSION_MAPPING = {
        "user-agent": None,
        "cryptocurrency-wallet": None,
        "cryptocurrency-transaction": None,
        "payment-card": None,
        "bank-account": None,
        "phone-number": None,
        "weakness": None,
    }
    EXTENSION_DEFINITION_BASE_URL = "https://raw.githubusercontent.com/muchdogesec/stix2extensions/main/automodel_generated/extension-definitions"
    ATTACK_FLOW_SMO_URL = "https://github.com/muchdogesec/stix2extensions/raw/refs/heads/main/remote-definitions/attack-flow.json"
    report = None
    identity = None
    object_marking_refs = []
    uuid = None
    id_map = dict()
    id_value_map = dict()
    _flow_objects = []
    default_identity = TXT2STIX_IDENTITY
    default_marking = TXT2STIX_MARKING

    def __init__(
        self,
        name,
        identity,
        tlp_level,
        description,
        confidence,
        extractors,
        labels,
        report_id=None,
        created=None,
        external_references=None,
        modified=None,
    ) -> None:
        self.observables_processed = 0
        self.created = created or dt.now(tz=UTC)
        self.all_extractors = extractors
        self.identity = identity or self.default_identity
        self.tlp_level = TLP_LEVEL.get(tlp_level)
        self.summary = ""
        if report_id:
            self.uuid = report_id
        else:
            self.uuid = str(
                uuid.uuid5(UUID_NAMESPACE, f"{self.identity.id}+{self.created}+{name}")
            )
        external_references = external_references or []
        labels = labels or []

        self.job_id = f"report--{self.uuid}"
        self.report_md5 = hashlib.md5(description.encode()).hexdigest()
        self.report = dict(
            type="report",
            spec_version="2.1",
            created_by_ref=self.identity.id,
            name=name,
            id=self.job_id,
            description=description,
            object_refs=[
            ],
            created=self.created,
            modified=modified or self.created,
            object_marking_refs=[self.tlp_level.value.id],
            labels=labels,
            published=self.created,
            external_references=[
                {
                    "source_name": "txt2stix_report_id",
                    "external_id": self.uuid,
                },
                {
                    "source_name": "txt2stix_report_md5",
                    "description": self.report_md5,
                },
            ]
            + external_references,
            confidence=confidence,
        )
        self.added_objects = set()
        self.set_defaults()

    def set_defaults(self):
        # self.value.extend(TLP_LEVEL.values()) # adds all tlp levels
        self.bundle = Bundle(objects=[self.tlp_level.value], id=f"bundle--{self.uuid}")

        self.bundle.objects.extend([self.default_marking, self.identity, self.report])
        # add default STIX 2.1 marking definition for txt2stix
        self.report["object_marking_refs"].append(self.default_marking.id)

    def add_extension(self, object):
        _type = object["type"]
        if self.EXTENSION_MAPPING.get(_type, "") is None:
            if isinstance(object, v21._Observable):
                url = self.EXTENSION_DEFINITION_BASE_URL + f"/scos/{_type}.json"
            elif isinstance(object, v21._DomainObject):
                url = self.EXTENSION_DEFINITION_BASE_URL + f"/sdos/{_type}.json"
            else:
                raise Exception(
                    f"Unknown custom object object.type = {_type}, {type(object)=}"
                )
            logger.info(f'getting extension definition for "{_type}" from `{url}`')
            self.EXTENSION_MAPPING[_type] = self.load_stix_object_from_url(url)
            extension = self.EXTENSION_MAPPING[_type]
            self.add_ref(extension, is_report_object=False)

    @staticmethod
    def load_stix_object_from_url(url):
        resp = requests.get(url)
        return dict_to_stix2(resp.json())

    def add_ref(self, sdo, is_report_object=True):
        self.add_extension(sdo)
        sdo_id = sdo["id"]
        if sdo_id not in self.added_objects:
            self.added_objects.add(sdo_id)
            if is_report_object:
                self.report["object_refs"].append(sdo_id)
            self.bundle.objects.append(sdo)

        sdo_value = ""
        for key in [
            "name",
            "value",
            "path",
            "key",
            "string",
            "number",
            "iban_number",
            "address",
            "hashes",
        ]:
            if v := sdo.get(key):
                sdo_value = v
                break
        else:
            if refs := sdo.get("external_references", []):
                sdo_value = refs[0]["external_id"]
            else:
                sdo_value = "{NOTEXTRACTED}"

        self.id_value_map[sdo_id] = sdo_value

    def add_indicator(self, extracted_dict, add_standard_relationship):
        extractor = self.all_extractors[extracted_dict["type"]]
        stix_mapping = extractor.stix_mapping
        extracted_value = extracted_dict["value"]
        extracted_id = extracted_dict["id"]

        if extracted_value is None or extracted_value == "":
            raise MinorException(f"extracted value is empty")

        indicator = self.new_indicator(extractor, stix_mapping, extracted_value)
        # set id so it doesn''t need to be created in build_observables
        if extracted_dict.get("indexes"):
            indicator["external_references"].append(
                dict(
                    source_name="indexes",
                    description=json.dumps(extracted_dict["indexes"]),
                )
            )
        objects, related_refs = build_observables(
            self, stix_mapping, indicator, extracted_dict["value"], extractor
        )
        if not objects:
            raise MinorException(
                f"build observable returns {objects} from extraction: {extracted_dict}"
            )
        self.id_map[extracted_id] = related_refs

        for sdo in objects:
            sdo = parse_stix(sdo, allow_custom=True)
            self.add_ref(sdo)

    def new_indicator(self, extractor, stix_mapping, extracted_value):
        indicator = {
            "type": "indicator",
            "id": self.indicator_id_from_value(extracted_value, stix_mapping),
            "spec_version": "2.1",
            "created_by_ref": self.report["created_by_ref"],
            "created": self.report["created"],
            "modified": self.report["modified"],
            "indicator_types": ["unknown"],
            "name": extracted_value,
            "pattern_type": "stix",
            "pattern": f"[ {stix_mapping}:value = { repr(extracted_value) } ]",
            "valid_from": self.report["created"],
            "object_marking_refs": self.report["object_marking_refs"],
            "external_references": [
                {
                    "source_name": "txt2stix_report_id",
                    "external_id": self.uuid,
                },
                {
                    "source_name": "txt2stix_extraction_type",
                    "description": f"{extractor.slug}_{extractor.version}",
                },
            ],
        }

        return indicator

    def add_ai_relationship(self, gpt_out):
        for source_ref in self.id_map.get(gpt_out["source_ref"], []):
            for target_ref in self.id_map.get(gpt_out["target_ref"], []):
                self.add_standard_relationship(
                    source_ref,
                    target_ref,
                    gpt_out["relationship_type"],
                )

    def add_standard_relationship(self, source_ref, target_ref, relationship_type):
        descriptor = " ".join(relationship_type.split("-"))
        self.add_ref(
            self.new_relationship(
                source_ref,
                target_ref,
                relationship_type,
                description=f"{self.id_value_map.get(source_ref, source_ref)} {descriptor} {self.id_value_map.get(target_ref, target_ref)}",
            )
        )

    def new_relationship(
        self,
        source_ref,
        target_ref,
        relationship_type,
        description=None,
        external_references=None,
    ):
        relationship = dict(
            id="relationship--"
            + str(
                uuid.uuid5(
                    UUID_NAMESPACE, f"{relationship_type}+{source_ref}+{target_ref}"
                )
            ),
            type="relationship",
            spec_version="2.1",
            source_ref=source_ref,
            target_ref=target_ref,
            relationship_type=relationship_type,
            created_by_ref=self.report["created_by_ref"],
            created=self.report["created"],
            description=description,
            modified=self.report["modified"],
            object_marking_refs=self.report["object_marking_refs"],
            external_references=external_references
            or [
                {
                    "source_name": "txt2stix_report_id",
                    "external_id": self.uuid,
                }
            ],
        )
        error = relationships_strict(relationship)
        if error:
            relationship["relationship_type"] = "related-to"
            logger.debug(error)
        return parse_stix(relationship, allow_custom=True)

    def to_json(self):
        report_index = self.bundle.objects.index(self.report)
        if not self.report['object_refs']:
            self.report['object_refs'] = [self.identity['id']]
        self.bundle.objects[report_index] = parse_stix(self.report, allow_custom=True)
        return serialize(self.bundle, indent=4)

    def process_observables(self, extractions, add_standard_relationship=False):
        for ex in extractions:
            try:
                ex["id"] = ex.get("id", f"ex_{self.observables_processed}")
                self.observables_processed += 1
                self.add_indicator(ex, add_standard_relationship)
            except BaseException as e:
                logger.debug(
                    f"ran into exception while processing observable `{ex}`. {e}",
                    exc_info=True,
                )
                ex["error"] = str(e)

    def process_relationships(self, observables):
        print(observables)
        for relationship in observables:
            try:
                self.add_ai_relationship(relationship)
            except BaseException as e:
                logger.debug(
                    f"ran into exception while processing relationship `{relationship}`",
                    stack_info=True,
                )

    def indicator_id_from_value(self, value, stix_mapping):
        return "indicator--" + str(
            uuid.uuid5(
                UUID_NAMESPACE,
                f"txt2stix+{self.identity['id']}+{self.report_md5}+{stix_mapping}+{value}",
            )
        )

    def add_summary(self, summary, ai_summary_provider):
        self.report["external_references"].append(
            dict(
                source_name="txt2stix_ai_summary",
                external_id=ai_summary_provider,
                description=summary,
            )
        )
        self.summary = summary

    @property
    def flow_objects(self):
        return self._flow_objects

    @flow_objects.setter
    def flow_objects(self, objects):
        smo_objects = self.load_stix_object_from_url(self.ATTACK_FLOW_SMO_URL)["objects"]
        objects.extend(smo_objects)
        for obj in objects:
            if obj["id"] == self.report["id"]:
                continue
            is_report_object = obj["type"] not in ["extension-definition", "identity"]
            self.add_ref(obj, is_report_object=is_report_object)
        self._flow_objects = objects
