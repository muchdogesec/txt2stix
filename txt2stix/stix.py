import enum
import logging
from stix2 import (
    Indicator,
    Report,
    Identity,
    Note,
    MarkingDefinition,
    Relationship,
    Bundle,
)
from stix2.parsing import dict_to_stix2, parse as parse_stix
from stix2.serialization import serialize
import codecs, base64
import hashlib
from stix2 import (
    NetworkTraffic,
    IPv4Address,
    IPv6Address,
    Indicator,
    File,
    DomainName,
    URL,
    Directory,
    EmailAddress,
    WindowsRegistryKey,
    AutonomousSystem,
)
import requests

from pathlib import Path

from .common import UUID_NAMESPACE, MinorExcption
from . import extractions
from datetime import datetime as dt
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
    EXTENSION_DEFINITION_BASE_URL = "https://raw.githubusercontent.com/muchdogesec/stix4doge/main/objects/extension-definition"
    report = None
    identity = None
    object_marking_refs = []
    uuid = None
    id_map = dict()
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
        job_id=None,
    ) -> None:
        self.whitelisted_values = set()
        self.whitelisted_refs = set()
        self.all_extractors = extractors
        self.identity = identity or self.default_identity
        self.tlp_level = TLP_LEVEL.get(tlp_level)
        self.uuid = job_id or str(uuid.uuid4())
        self.job_id = f"report--{self.uuid}"
        self.report = Report(
            created_by_ref=self.identity.id,
            name=name,
            id=self.job_id,
            description=description,
            object_refs=[
                f"note--{self.uuid}"
            ],  # won't allow creation with empty object_refs
            object_marking_refs=[self.tlp_level.value.id],
            labels=labels,
            published=dt.now(),
            external_references=[
                {
                    "source_name": "txt2stix job ID",
                    "description": self.job_id,
                },
                {
                    "source_name": "txt2stix Report MD5",
                    "external_id": hashlib.md5(description.encode()).hexdigest(),
                },
            ],
            confidence=confidence,
        )
        self.report.object_refs.clear()  # clear object refs
        self.set_defaults()

    def set_defaults(self):
        # self.value.extend(TLP_LEVEL.values()) # adds all tlp levels
        self.bundle = Bundle(objects=[self.tlp_level.value], id=f"bundle--{self.uuid}")

        self.bundle.objects.extend([self.default_marking, self.identity, self.report])
        # add default STIX 2.1 marking definition for txt2stix
        self.report.object_marking_refs.append(self.default_marking.id)
        # add import tlp:red for notes if it's not imported already
        if self.tlp_level != TLP_LEVEL.RED:
            self.bundle.objects.append(TLP_LEVEL.RED.value)

    def add_extension(self, object):
        _type = object["type"]
        if self.EXTENSION_MAPPING.get(_type, "") is None:
            url = self.EXTENSION_DEFINITION_BASE_URL + f"/{_type}.json"
            logger.info(f'getting extension definition for "{_type}" from `{url}`')
            self.EXTENSION_MAPPING[_type] = self.load_object_from_json(url)
            extension = self.EXTENSION_MAPPING[_type]
            self.add_ref(extension)

    @staticmethod
    def load_object_from_json(url):
        resp = requests.get(url)
        return dict_to_stix2(resp.json())

    def add_note(self, content, type):
        content, _ = codecs.utf_8_encode(content)
        note = Note(
            created=self.report.created,
            modified=self.report.modified,
            abstract=f"txt2stix {type}: {self.job_id}",
            content=base64.b64encode(content).decode(),
            object_refs=[self.report.id],
            created_by_ref=self.report.created_by_ref,
            object_marking_refs=[
                "marking-definition--e828b379-4e03-4974-9ac4-e53a884c97c1",
                "marking-definition--f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5",
            ],
            external_references=[
                {"source_name": "txt2stix job ID", "external_id": self.job_id}
            ],
        )

        self.bundle.objects.append(note)

    def add_ref(self, sdo):
        self.add_extension(sdo)
        sdo_id = sdo["id"]
        if sdo_id not in self.report.object_refs:
            self.report.object_refs.append(sdo_id)
            self.bundle.objects.append(sdo)

    def add_indicator(self, extracted_dict, add_standard_relationship):
        extractor = self.all_extractors[extracted_dict["type"]]
        stix_mapping = extractor.stix_mapping
        extracted_value = extracted_dict["value"]
        extracted_id = extracted_dict["id"]
        if extracted_value in self.whitelisted_values:
            self.whitelisted_refs.add(extracted_id)
            return
        # print(stix_mapping, gpt_out)
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
                    "source_name": "txt2stix job ID",
                    "description": self.job_id,
                },
                {
                    "source_name": "txt2stix extraction ID",
                    "description": f"{extractor.slug}_{extractor.version}",
                },
            ],
        }
        # set id so it doesn''t need to be created in build_observables
        if extracted_dict.get("indexes"):
            indicator["external_references"].append(
                dict(
                    source_name="indexes",
                    description=json.dumps(extracted_dict["indexes"]),
                )
            )
        objects, related_refs = build_observables(
            self, stix_mapping, indicator, extracted_dict, extractor
        )
        if not objects:
            raise MinorExcption(
                f"build observable returns {objects} from extraction: {extracted_dict}"
            )
        self.id_map[extracted_id] = related_refs

        for sdo in objects:
            sdo = parse_stix(sdo, allow_custom=True)
            self.add_ref(sdo)

        # if add_standard_relationship and not indicator:
        #     for r in related_refs:
        #         self.add_standard_relationship(
        #             r["id"], self.report.id, "extracted-from"
        #         )
        # elif add_standard_relationship:
        #     self.add_standard_relationship(
        #         objects[0].id, self.report.id, "extracted-from"
        #     )

    def add_ai_relationship(self, gpt_out):
        if (
            gpt_out["source_ref"] in self.whitelisted_refs
            or gpt_out["target_ref"] in self.whitelisted_refs
        ):
            return

        for source_ref in self.id_map.get(gpt_out["source_ref"]):
            for target_ref in self.id_map.get(gpt_out["target_ref"]):
                self.add_standard_relationship(
                    source_ref, target_ref, gpt_out["relationship_type"]
                )

    def add_standard_relationship(self, source_ref, target_ref, relationship_type):
        self.add_ref(self.new_relationship(source_ref, target_ref, relationship_type))

    def new_relationship(self, source_ref, target_ref, relationship_type):
        return Relationship(
            id="relationship--" + str(
                uuid.uuid5(
                    UUID_NAMESPACE, f"{relationship_type}+{source_ref}+{target_ref}"
                )
            ),
            source_ref=source_ref,
            target_ref=target_ref,
            relationship_type=relationship_type,
            created_by_ref=self.report.created_by_ref,
            created=self.report.created,
            modified=self.report.modified,
            object_marking_refs=self.report.object_marking_refs,
            allow_custom=True,
            external_references=[
                {
                    "source_name": "txt2stix job ID",
                    "external_id": self.job_id,
                }
            ],
        )

    def to_json(self):
        return serialize(self.bundle, pretty=True)

    def process_observables(self, extractions, add_standard_relationship=False):
        self.objects_count = getattr(self, 'objects_count', 0)
        for ex in extractions:
            try:
                ex["id"] = ex.get('id', f"ex_{self.objects_count}")
                self.objects_count += 1
                self.add_indicator(ex, add_standard_relationship)
            except BaseException as e:
                logger.exception(
                    f"ran into exception while processing observable `{ex}`",
                    stack_info=True,
                )

    def process_relationships(self, observables):
        for relationship in observables:
            try:
                self.add_ai_relationship(relationship)
            except BaseException as e:
                logger.exception(
                    f"ran into exception while processing relationship `{relationship}`",
                    stack_info=True,
                )

    @staticmethod
    def indicator_id_from_value(value, stix_mapping):
        return "indicator--" + str(
            uuid.uuid5(UUID_NAMESPACE, f"txt2stix+{stix_mapping}+{value}")
        )
