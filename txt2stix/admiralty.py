import enum
from functools import lru_cache
import json
import urllib.error
import urllib.parse
import urllib.request
import requests

from stix2.parsing import dict_to_stix2

BASE_URL = "https://downloads.ctibutler.com/admiralty-codes/objects"
SOURCE_RELIABILITY_PROPERTY = "source-reliability"
INFORMATION_CREDIBILITY_PROPERTY = "information-credibility"


def _object_url(property_name: str, stix_id: str) -> str:
    _type, _, _ = stix_id.partition("--")
    if "marking-definition" == _type:
        property_name = urllib.parse.quote(property_name, safe="")
        stix_id = urllib.parse.quote(stix_id, safe="-")
        return f"{BASE_URL}/marking-definition/{property_name}/{stix_id}.json"
    
    return f"{BASE_URL}/{_type}/{stix_id}.json"


ADMIRALTY__OBJECTS = {}

@lru_cache(maxsize=1)
def prepare():
    url = f"{BASE_URL}/bundle/all_objects_bundle.json"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    bundle = dict_to_stix2(data, allow_custom=True)
    for obj in bundle.objects:
        ADMIRALTY__OBJECTS[obj.id] = obj
        if obj.type == "extension-definition":
            if "admiralty_source_reliability" in obj.extension_properties:
                ADMIRALTY_SOURCE_RELIABILITY.extension_definition = obj
            elif "admiralty_information_credibility" in obj.extension_properties:
                ADMIRALTY_INFORMATION_CREDIBILITY.extension_definition = obj

class _AdmiraltyEnum(enum.Enum):
    # extension_definition = None
    def __new__(cls, property_name: str, stix_id: str):
        member = object.__new__(cls)
        member._value_ = stix_id
        member.property_name = property_name
        member.stix_id = stix_id
        return member

    @property
    def value(self):
        prepare()
        return ADMIRALTY__OBJECTS[self.stix_id]

    @property
    def objects(self):
        value = self.value
        yield self.extension_definition
        for k, v in value.items():
            if k in ["created_by_ref", "object_marking_refs"]:
                if isinstance(v, str):
                    v = [v]
                for item in v:
                    if item in ADMIRALTY__OBJECTS:
                        yield ADMIRALTY__OBJECTS[item]
        yield value

    @classmethod
    def levels(cls):
        return {item.name: item for item in cls}

    @classmethod
    def values(cls):
        return [item.value for item in cls]

    @classmethod
    def get(cls, level):
        if isinstance(level, cls):
            return level
        return cls.levels()[str(level).upper()]


class ADMIRALTY_SOURCE_RELIABILITY(_AdmiraltyEnum):
    A = (
        SOURCE_RELIABILITY_PROPERTY,
        "marking-definition--cf438540-077a-56c7-b68e-82fcc2bb0208",
    )
    B = (
        SOURCE_RELIABILITY_PROPERTY,
        "marking-definition--b3cd9dd0-9081-5cbe-84d0-ef5bc11b8b13",
    )
    C = (
        SOURCE_RELIABILITY_PROPERTY,
        "marking-definition--3545f856-c5f5-5d2f-a1ae-102e0b6028b2",
    )
    D = (
        SOURCE_RELIABILITY_PROPERTY,
        "marking-definition--223ecfcc-22ce-5ece-b91c-a05a53a91959",
    )
    E = (
        SOURCE_RELIABILITY_PROPERTY,
        "marking-definition--9eff5f66-33b9-5e54-9868-72179b28ae12",
    )
    F = (
        SOURCE_RELIABILITY_PROPERTY,
        "marking-definition--adebda39-90c9-5ac0-9107-c26d86a6c3d8",
    )


class ADMIRALTY_INFORMATION_CREDIBILITY(_AdmiraltyEnum):
    _1 = (
        INFORMATION_CREDIBILITY_PROPERTY,
        "marking-definition--2462b621-0825-5879-917c-082e0394bcf4",
    )
    _2 = (
        INFORMATION_CREDIBILITY_PROPERTY,
        "marking-definition--9cf59b27-57f8-5250-98f4-16c462d5652c",
    )
    _3 = (
        INFORMATION_CREDIBILITY_PROPERTY,
        "marking-definition--4c76ec83-d905-5ada-b0bf-8ae2fb9e9f4d",
    )
    _4 = (
        INFORMATION_CREDIBILITY_PROPERTY,
        "marking-definition--c36a018d-bc8e-57a4-a39d-9e7e31d1bc17",
    )
    _5 = (
        INFORMATION_CREDIBILITY_PROPERTY,
        "marking-definition--0a48adab-e7d5-5354-8a41-abf199fe2628",
    )
    _6 = (
        INFORMATION_CREDIBILITY_PROPERTY,
        "marking-definition--2244db4b-ee29-5b8c-bed4-c7ac784c647a",
    )

    @classmethod
    def levels(cls):
        return {item.name.removeprefix("_"): item for item in cls}
