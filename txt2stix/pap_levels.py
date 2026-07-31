import enum
from stix2 import ExtensionDefinition, MarkingDefinition

from .common import CISA_IDENTITY, CISA_IDENTITY_ID

# https://github.com/oasis-open/cti-stix-common-objects/tree/main/extension-definition-specifications/pap-marking-definition-f8d
PAP_EXTENSION_DEFINITION_ID = "extension-definition--f8d78575-edfd-406e-8e84-6162a8450f5b"
PAP_EXTENSION_DEFINITION = ExtensionDefinition(
    id=PAP_EXTENSION_DEFINITION_ID,
    type="extension-definition",
    spec_version="2.1",
    name="PAP",
    description="This defines PAP as a STIX extension",
    created="2022-11-28T00:00:00.000Z",
    modified="2022-11-28T00:00:00.000Z",
    created_by_ref=CISA_IDENTITY_ID,
    schema="https://github.com/oasis-open/cti-stix-common-objects/tree/master/extension-definition-specifications/pap",
    version="1.0.0",
    extension_types=["property-extension"],
)


class PAP_LEVEL(enum.Enum):
    CLEAR = MarkingDefinition(
        type="marking-definition",
        spec_version="2.1",
        id="marking-definition--ad15a0cd-55b6-4588-a14c-a66105329b92",
        created="2022-10-01T00:00:00.000Z",
        name="PAP:CLEAR",
        extensions={
            PAP_EXTENSION_DEFINITION_ID: {
                "extension_type": "property-extension",
                "pap": "clear",
            }
        },
    )
    GREEN = MarkingDefinition(
        type="marking-definition",
        spec_version="2.1",
        id="marking-definition--c43594d1-4b11-4c59-93ab-1c9b14d53ce9",
        created="2022-10-09T00:00:00.000Z",
        name="PAP:GREEN",
        extensions={
            PAP_EXTENSION_DEFINITION_ID: {
                "extension_type": "property-extension",
                "pap": "green",
            }
        },
    )
    AMBER = MarkingDefinition(
        type="marking-definition",
        spec_version="2.1",
        id="marking-definition--60f8932b-e51e-4458-b265-a2e8be9a80ab",
        created="2022-10-02T00:00:00.000Z",
        name="PAP:AMBER",
        extensions={
            PAP_EXTENSION_DEFINITION_ID: {
                "extension_type": "property-extension",
                "pap": "amber",
            }
        },
    )
    RED = MarkingDefinition(
        type="marking-definition",
        spec_version="2.1",
        id="marking-definition--740d36e5-7714-4c30-961a-3ae632ceee0e",
        created="2022-10-06T00:00:00.000Z",
        name="PAP:RED",
        extensions={
            PAP_EXTENSION_DEFINITION_ID: {
                "extension_type": "property-extension",
                "pap": "red",
            }
        },
    )
    # legacy value, retained for older MISP compatibility. Prefer CLEAR.
    WHITE = MarkingDefinition(
        type="marking-definition",
        spec_version="2.1",
        id="marking-definition--a3bea94c-b469-41dc-9cfe-d6e7daba7730",
        created="2022-10-01T00:00:00.000Z",
        name="PAP:WHITE",
        extensions={
            PAP_EXTENSION_DEFINITION_ID: {
                "extension_type": "property-extension",
                "pap": "white",
            }
        },
    )

    @classmethod
    def levels(cls):
        return dict(
            clear=cls.CLEAR,
            green=cls.GREEN,
            amber=cls.AMBER,
            red=cls.RED,
            white=cls.WHITE,
        )

    @classmethod
    def values(cls):
        return [
            cls.CLEAR.value,
            cls.GREEN.value,
            cls.AMBER.value,
            cls.RED.value,
            cls.WHITE.value,
        ]

    @classmethod
    def get(cls, level):
        if isinstance(level, cls):
            return level
        return cls.levels()[str(level).lower()]

    @property
    def name(self):
        return super().name.lower()

    @property
    def objects(self):
        yield PAP_EXTENSION_DEFINITION
        yield CISA_IDENTITY
        yield self.value
