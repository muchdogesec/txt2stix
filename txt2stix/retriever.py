import logging
from urllib.parse import urljoin
import dotenv, os
import stix2
import requests

from txt2stix.common import MinorException

dotenv.load_dotenv()


class UnsupportedRemoteExtraction(MinorException):
    pass


class STIXObjectRetriever:
    def __init__(self, host="ctibutler") -> None:
        if host == "ctibutler":
            self.api_root = os.environ["CTIBUTLER_BASE_URL"] + "/"
            self.api_key = os.environ.get("CTIBUTLER_API_KEY")
        elif host == "vulmatch":
            self.api_root = os.environ["VULMATCH_BASE_URL"] + "/"
            self.api_key = os.environ.get("VULMATCH_API_KEY")
        else:
            raise UnsupportedRemoteExtraction("The type `%s` is not supported", host)

        self.session = requests.Session()
        self.session.headers.update(
            {
                "API-KEY": self.api_key,
            }
        )

    def get_attack_object(self, matrix, attack_id):
        endpoint = urljoin(self.api_root, f"v1/attack-{matrix}/objects/{attack_id}/")
        return self._retrieve_objects(endpoint)

    def get_attack_tactics(self, matrix):
        endpoint = urljoin(
            self.api_root, f"v1/attack-{matrix}/objects/?attack_type=Tactic"
        )
        version_url = urljoin(self.api_root, f"v1/attack-{matrix}/versions/installed/")
        tactics = self._retrieve_objects(endpoint)
        retval = dict(version=self.session.get(version_url).json()["latest"])
        for tac in tactics:
            retval[tac["x_mitre_shortname"]] = tac
            retval[tac["external_references"][0]["external_id"]] = tac
        return retval

    def get_attack_objects(self, matrix, attack_ids):
        endpoint = urljoin(
            self.api_root,
            f"v1/attack-{matrix}/objects/?attack_id={','.join(attack_ids)}",
        )
        return self._retrieve_objects(endpoint)

    def get_objects_by_id(self, id, type):
        return self._retrieve_objects(
            urljoin(self.api_root, f"v1/{type}/objects/{id}/")
        )
    
    def retrieve_object_by_id(self, id, type):
        endpoint = urljoin(self.api_root, f"v1/{type}/objects/{id}/")
        resp = self.session.get(endpoint)
        resp.raise_for_status()
        return [resp.json()]

    def get_location_objects(self, id):
        return self._retrieve_objects(
            urljoin(self.api_root, f"v1/location/objects/?alpha2_code={id}")
        )

    def get_objects_by_name(self, name, type):
        return self._retrieve_objects(
            urljoin(self.api_root, f"v1/{type}/objects/?name={name}")
        )

    def get_objects_by_alias(self, alias, type):
        return self._retrieve_objects(
            urljoin(self.api_root, f"v1/{type}/objects/?alias={alias}")
        )

    def _retrieve_objects(self, endpoint, key="objects"):
        data = []
        page = 1
        while True:
            resp = self.session.get(endpoint, params=dict(page=page, page_size=50))
            resp.raise_for_status()
            d = resp.json()
            if len(d[key]) == 0:
                break
            data.extend(d[key])
            page += 1
            if d["page_results_count"] < d["page_size"]:
                break
        return data


def _retrieve_stix_objects(host, knowledge_base, filter_value):
    retreiver = STIXObjectRetriever(host)
    match knowledge_base:
        ### ATT&CK by ID
        case "mitre-attack-ics-id":
            return retreiver.get_attack_object("ics", filter_value)
        case "mitre-attack-mobile-id":
            return retreiver.get_attack_object("mobile", filter_value)
        case "mitre-attack-enterprise-id":
            return retreiver.get_attack_object("enterprise", filter_value)

        ### Others by ID
        case "mitre-capec-id":
            return retreiver.get_objects_by_id(filter_value, "capec")
        case "mitre-atlas-id":
            return retreiver.get_objects_by_id(filter_value, "atlas")
        case "disarm-id":
            return retreiver.get_objects_by_id(filter_value, "disarm")
        case "mitre-cwe-id":
            return retreiver.get_objects_by_id(filter_value, "cwe")
        case "cve-id":
            return retreiver.retrieve_object_by_id(filter_value, "cve")
        case "cpe-id":
            return retreiver.retrieve_object_by_id(filter_value, "cpe")
        case "location":
            return retreiver.get_location_objects(filter_value)

        ### ATT&CK by Name
        case "mitre-attack-enterprise-name":
            return retreiver.get_objects_by_name(filter_value, "attack-enterprise")
        case "mitre-attack-mobile-name":
            return retreiver.get_objects_by_name(filter_value, "attack-mobile")
        case "mitre-attack-ics-name":
            return retreiver.get_objects_by_name(filter_value, "attack-ics")

        ### ATT&CK by Alias
        case "mitre-attack-enterprise-aliases":
            return retreiver.get_objects_by_alias(filter_value, "attack-enterprise")
        case "mitre-attack-mobile-aliases":
            return retreiver.get_objects_by_alias(filter_value, "attack-mobile")
        case "mitre-attack-ics-aliases":
            return retreiver.get_objects_by_alias(filter_value, "attack-ics")

        ### OTHERS by Name
        case "mitre-capec-name":
            return retreiver.get_objects_by_name(filter_value, "capec")
        case "mitre-cwe-name":
            return retreiver.get_objects_by_name(filter_value, "cwe")
        case "mitre-atlas-name":
            return retreiver.get_objects_by_name(filter_value, "atlas")
        case "disarm-name":
            return retreiver.get_objects_by_name(filter_value, "disarm")
        case _:
            raise UnsupportedRemoteExtraction(
                f"pair {(host, knowledge_base)=} not implemented"
            )


def retrieve_stix_objects(stix_mapping: str, filter_value, host=None):
    knowledge_base = stix_mapping
    if stix_mapping in ["location"]:
        host = "ctibutler"
    if not host:
        host, _, knowledge_base = stix_mapping.partition("-")
    try:
        objects = _retrieve_stix_objects(host, knowledge_base, filter_value)
        if not objects:
            raise MinorException(f"{host} returned no data")
        if len(objects)> 15:
            raise MinorException(f"{host} returned too much data ({len(objects)})")
        return objects
    except UnsupportedRemoteExtraction:
        return None
