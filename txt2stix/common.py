from typing import Any
from uuid import UUID
from stix2 import Identity, MarkingDefinition

UUID_NAMESPACE = UUID("f92e15d9-6afc-5ae2-bb3e-85a1fd83a3b5")
DOGESEC_IDENTITY_ID = "identity--9779a2db-f98c-5f4b-8d08-8ee04e02dbb5"

TXT2STIX_IDENTITY = Identity(
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
TXT2STIX_MARKING = MarkingDefinition(
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

class NamedDict(dict):
    def __getattribute__(self, attr: str):
        value = None
        try:
            value = super().__getattribute__(attr)
        except:
            pass
        if value is not None:
            return value
        return super().get(attr, "")

    def __setattr__(self, __name: str, __value: Any) -> None:
        return super().__setitem__(__name, __value)

class FatalException(Exception):
    pass
class MinorException(Exception):
    pass
