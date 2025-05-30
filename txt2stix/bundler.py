import enum
import logging
from stix2 import (
    Report,
    Identity,
    MarkingDefinition,
    Relationship,
    Bundle,
)
from stix2.parsing import dict_to_stix2, parse as parse_stix
from stix2.serialization import serialize
import hashlib
from stix2 import (
    v21,
)
import requests


from .common import UUID_NAMESPACE, MinorException
from datetime import UTC, datetime as dt
import uuid
import json
from .indicator import build_observables


logger = logging.getLogger("txt2stix.stix")


class TLP_LEVEL(enum.Enum):
    CLEAR = MarkingDefinition(
        spec_version="2.1",
        id="marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487",
        created="2022-10-01T00:00:00.000Z",
        definition_type="TLP:CLEAR",
        extensions={
            "extension-definition--60a3c5c5-0d10-413e-aab3-9e08dde9e88d": {
                "extension_type": "property-extension",
                "tlp_2_0": "clear",
            }
        },
    )
    GREEN = MarkingDefinition(
        spec_version="2.1",
        id="marking-definition--bab4a63c-aed9-4cf5-a766-dfca5abac2bb",
        created="2022-10-01T00:00:00.000Z",
        definition_type="TLP:GREEN",
        extensions={
            "extension-definition--60a3c5c5-0d10-413e-aab3-9e08dde9e88d": {
                "extension_type": "property-extension",
                "tlp_2_0": "green",
            }
        },
    )
    AMBER = MarkingDefinition(
        spec_version="2.1",
        id="marking-definition--55d920b0-5e8b-4f79-9ee9-91f868d9b421",
        created="2022-10-01T00:00:00.000Z",
        definition_type="TLP:AMBER",
        extensions={
            "extension-definition--60a3c5c5-0d10-413e-aab3-9e08dde9e88d": {
                "extension_type": "property-extension",
                "tlp_2_0": "amber",
            }
        },
    )
    AMBER_STRICT = MarkingDefinition(
        spec_version="2.1",
        id="marking-definition--939a9414-2ddd-4d32-a0cd-375ea402b003",
        created="2022-10-01T00:00:00.000Z",
        definition_type="TLP:AMBER+STRICT",
        extensions={
            "extension-definition--60a3c5c5-0d10-413e-aab3-9e08dde9e88d": {
                "extension_type": "property-extension",
                "tlp_2_0": "amber+strict",
            }
        },
    )
    RED = MarkingDefinition(
        spec_version="2.1",
        id="marking-definition--e828b379-4e03-4974-9ac4-e53a884c97c1",
        created="2022-10-01T00:00:00.000Z",
        definition_type="TLP:RED",
        extensions={
            "extension-definition--60a3c5c5-0d10-413e-aab3-9e08dde9e88d": {
                "extension_type": "property-extension",
                "tlp_2_0": "red",
            }
        },
    )

    @classmethod
    def levels(cls):
        return dict(
            clear=cls.CLEAR,
            green=cls.GREEN,
            amber=cls.AMBER,
            amber_strict=cls.AMBER_STRICT,
            red=cls.RED,
        )

    @classmethod
    def values(cls):
        return [
            cls.CLEAR.value,
            cls.GREEN.value,
            cls.AMBER.value,
            cls.AMBER_STRICT.value,
            cls.RED.value,
        ]

    @classmethod
    def get(cls, level):
        if isinstance(level, cls):
            return level
        return cls.levels()[level]

    @property
    def name(self):
        return super().name.lower()


class txt2stixBundler:
    EXTENSION_MAPPING = {
        "user-agent": None,
        "cryptocurrency-wallet": None,
        "cryptocurrency-transaction": None,
        "bank-card": None,
        "bank-account": None,
        "phone-number": None,
        "weakness": None,
    }
    EXTENSION_DEFINITION_BASE_URL = "https://raw.githubusercontent.com/muchdogesec/stix2extensions/main/extension-definitions"
    report = None
    identity = None
    object_marking_refs = []
    uuid = None
    id_map = dict()
    id_value_map = dict()
    _flow_objects = []
    # this identity is https://raw.githubusercontent.com/muchdogesec/stix4doge/main/objects/identity/txt2stix.json
    default_identity = Identity(
        type="identity",
        spec_version="2.1",
        id="identity--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5",
        created_by_ref="identity--9779a2db-f98c-5f4b-8d08-8ee04e02dbb5",
        created="2020-01-01T00:00:00.000Z",
        modified="2020-01-01T00:00:00.000Z",
        name="txt2stix",
        description="https://github.com/muchdogsec/txt2stix",
        identity_class="system",
        sectors=["technology"],
        contact_information="https://www.dogesec.com/contact/",
        object_marking_refs=[
            "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487",
            "marking-definition--97ba4e8b-04f6-57e8-8f6e-3a0f0a7dc0fb",
        ],
    )
    # this marking-definition is https://raw.githubusercontent.com/muchdogesec/stix4doge/main/objects/marking-definition/txt2stix.json
    default_marking = MarkingDefinition(
        type="marking-definition",
        spec_version="2.1",
        id="marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5",
        created_by_ref="identity--9779a2db-f98c-5f4b-8d08-8ee04e02dbb5",
        created="2020-01-01T00:00:00.000Z",
        definition_type="statement",
        definition={
            "statement": "This object was created using: https://github.com/muchdogesec/txt2stix"
        },
        object_marking_refs=[
            "marking-definition--94868c89-83c2-464b-929b-a1a8aa3c8487",
            "marking-definition--97ba4e8b-04f6-57e8-8f6e-3a0f0a7dc0fb",
        ],
    )

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
        if report_id:
            self.uuid = report_id
        else:
            self.uuid = str(
                uuid.uuid5(UUID_NAMESPACE, f"{self.identity.id}+{self.created}+{name}")
            )
        external_references = external_references or []
        labels = labels or []
        labels.append('placeholder_label')

        self.job_id = f"report--{self.uuid}"
        self.report_md5 = hashlib.md5(description.encode()).hexdigest()
        self.report = Report(
            created_by_ref=self.identity.id,
            name=name,
            id=self.job_id,
            description=description,
            object_refs=[
                f"note--{self.uuid}"
            ],  # won't allow creation with empty object_refs
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
                    "source_name": "txt2stix Report MD5",
                    "description": self.report_md5,
                },
            ] + external_references,
            confidence=confidence,
        )
        self.report.object_refs.clear()  # clear object refs
        self.report.labels.pop(-1) # remove txt2stix placeholder
        self.added_objects = set()
        self.set_defaults()

    def set_defaults(self):
        # self.value.extend(TLP_LEVEL.values()) # adds all tlp levels
        self.bundle = Bundle(objects=[self.tlp_level.value], id=f"bundle--{self.uuid}")

        self.bundle.objects.extend([self.default_marking, self.identity, self.report])
        # add default STIX 2.1 marking definition for txt2stix
        self.report.object_marking_refs.append(self.default_marking.id)

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
                self.report.object_refs.append(sdo_id)
            self.bundle.objects.append(sdo)

        sdo_value = ""
        for key in ['name', 'value', 'path', 'key', 'string', 'number', 'iban_number', 'address', 'hashes']:
            if v := sdo.get(key):
                sdo_value = v
                break
        else:
            if refs := sdo.get('external_references', []):
                sdo_value = refs[0]['external_id']
            else:
                sdo_value = "{NOTEXTRACTED}"


        self.id_value_map[sdo_id] = sdo_value


    def add_indicator(self, extracted_dict, add_standard_relationship):
        extractor = self.all_extractors[extracted_dict["type"]]
        stix_mapping = extractor.stix_mapping
        extracted_value = extracted_dict["value"]
        extracted_id = extracted_dict["id"]


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
            self, stix_mapping, indicator, extracted_dict['value'], extractor
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
            "created_by_ref": self.report.created_by_ref,
            "created": self.report.created,
            "modified": self.report.modified,
            "indicator_types": ["unknown"],
            "name": extracted_value,
            "pattern_type": "stix",
            "pattern": f"[ {stix_mapping}:value = { repr(extracted_value) } ]",
            "valid_from": self.report.created,
            "object_marking_refs": self.report.object_marking_refs,
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
                    source_ref, target_ref, gpt_out["relationship_type"],
                )

    def add_standard_relationship(self, source_ref, target_ref, relationship_type):
        descriptor = ' '.join(relationship_type.split('-'))
        self.add_ref(self.new_relationship(
            source_ref, target_ref, relationship_type,
            description=f"{self.id_value_map.get(source_ref, source_ref)} {descriptor} {self.id_value_map.get(target_ref, target_ref)}"
        ))

    def new_relationship(self, source_ref, target_ref, relationship_type, description=None, external_references=None):
        return Relationship(
            id="relationship--"
            + str(
                uuid.uuid5(
                    UUID_NAMESPACE, f"{relationship_type}+{source_ref}+{target_ref}"
                )
            ),
            source_ref=source_ref,
            target_ref=target_ref,
            relationship_type=relationship_type,
            created_by_ref=self.report.created_by_ref,
            created=self.report.created,
            description=description,
            modified=self.report.modified,
            object_marking_refs=self.report.object_marking_refs,
            allow_custom=True,
            external_references=external_references or [
                {
                    "source_name": "txt2stix_report_id",
                    "external_id": self.uuid,
                }
            ],
        )

    def to_json(self):
        return serialize(self.bundle, indent=4)

    def process_observables(self, extractions, add_standard_relationship=False):
        for ex in extractions:
            try:
                if ex.get('id', '').startswith('ai'): #so id is distinct across multiple AIExtractors
                    ex["id"] = f'{ex["id"]}_{self.observables_processed}'
                ex["id"] = ex.get("id", f"ex_{self.observables_processed}")
                self.observables_processed += 1
                self.add_indicator(ex, add_standard_relationship)
            except BaseException as e:
                logger.debug(
                    f"ran into exception while processing observable `{ex}`",
                    stack_info=True,
                )

    def process_relationships(self, observables):
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
            uuid.uuid5(UUID_NAMESPACE, f"txt2stix+{self.identity['id']}+{self.report_md5}+{stix_mapping}+{value}")
        )
    
    @property
    def flow_objects(self):
        return self._flow_objects
    
    @flow_objects.setter
    def flow_objects(self, objects):
        for obj in objects:
            if obj['id'] == self.report.id:
                continue
            is_report_object = obj['type'] != "extension-definition"
            self.add_ref(obj, is_report_object=is_report_object)
        self._flow_objects = objects