import os
import json, re
from stix2.parsing import dict_to_stix2, parse as parse_stix
from stix2 import IPv4Address, CustomObject, CustomObservable, File, HashConstant
from stix2.v21.vocab import HASHING_ALGORITHM
from stix2.patterns import _HASH_REGEX as HASHING_ALGORITHM_2
from urllib.parse import urlparse
from ipaddress import ip_address
from pathlib import PurePosixPath, PureWindowsPath
import phonenumbers
from phonenumbers import geocoder
import logging
from stix4doge import (
    BankAccount,
    BankCard,
    CryptocurrencyTransaction,
    CryptocurrencyWallet,
    Phonenumber,
    UserAgent,
    Weakness,
)
from stix4doge.tools import creditcard2stix, crypto2stix

# from schwifty import IBAN

from .common import MinorExcption

from .arangodb import ArangoSession

logger = logging.getLogger("txt2stix.indicator")


def find_hash_type(value, name):
    for alg in HASHING_ALGORITHM + ["SHA-384"]:
        if alg.upper() in name.upper():
            return alg
    for _, alg in HASHING_ALGORITHM_2.values():
        try:
            HashConstant(value, alg)
            return alg
        except:
            pass
    return


class ParseObservableError(Exception):
    pass


def parse_path(pathstr):
    path = PureWindowsPath(pathstr)
    if pathstr == path.as_posix():
        return PurePosixPath(pathstr)
    return path


def split_ip_port(ip_port):
    ip, port = ip_port.rsplit(":", 1)
    ip = ip.replace("[", "").replace("]", "")  # remove the [] enclosuure if it's ipv6
    ip = ip_address(ip)

    return ip.exploded, int(port)


def get_country_code(number: str) -> str:
    try:
        if not number.startswith("+"):
            number = "+" + number
        phone = phonenumbers.parse(number, None)
        return geocoder.region_codes_for_country_code(phone.country_code)[0]
    except:
        return None


def get_iban_details(number) -> tuple[str, str]:
    return number[:2], None


def build_observables(bundler, stix_mapping, indicator, extracted, extractor):
    value = extracted["value"]

    arango_objects = arangodb_check(stix_mapping, value)
    if arango_objects:
        return arango_objects, [sdo["id"] for sdo in arango_objects]
    if arango_objects == []:
        logger.error(
            f"could not find `{stix_mapping}` with value `{value}` in ArangoDB"
        )
        return [], []

    stix_objects = [indicator]

    if stix_mapping == "ipv4-addr":
        indicator["name"] = f"ipv4: {value}"
        indicator["pattern"] = f"[ ipv4-addr:value = { repr(value) } ]"

        stix_objects.append(
            dict_to_stix2({"type": "ipv4-addr", "spec_version": "2.1", "value": value})
        )

        stix_objects.append(
            bundler.new_relationship(stix_objects[1].id, indicator["id"], "related-to")
        )

    if stix_mapping == "ipv4-addr-port":
        value, port = split_ip_port(value)
        indicator["name"] = f"ipv4: {value}"
        indicator["pattern"] = f"[ ipv4-addr:value = { repr(value) } ]"

        stix_objects.append(
            dict_to_stix2({"type": "ipv4-addr", "spec_version": "2.1", "value": value})
        )
        id = stix_objects[-1].id
        stix_objects.append(
            bundler.new_relationship(stix_objects[1].id, indicator["id"], "related-to")
        )

        stix_objects.append(
            dict_to_stix2(
                {
                    "type": "network-traffic",
                    "spec_version": "2.1",
                    "dst_ref": id,
                    "dst_port": port,
                    "protocols": ["ipv4"],
                }
            )
        )

    if stix_mapping == "ipv6-addr":
        indicator["name"] = f"ipv6: {value}"
        indicator["pattern"] = f"[ ipv6-addr:value = { repr(value) } ]"

        stix_objects.append(
            dict_to_stix2({"type": "ipv6-addr", "spec_version": "2.1", "value": value})
        )
        stix_objects.append(
            bundler.new_relationship(stix_objects[1].id, indicator["id"], "related-to")
        )

    if stix_mapping == "ipv6-addr-port":
        value, port = split_ip_port(value)
        indicator["name"] = f"ipv6: {value}"
        indicator["pattern"] = f"[ ipv6-addr:value = { repr(value) } ]"

        stix_objects.append(
            dict_to_stix2({"type": "ipv6-addr", "spec_version": "2.1", "value": value})
        )
        id = stix_objects[-1].id
        stix_objects.append(
            bundler.new_relationship(stix_objects[1].id, indicator["id"], "related-to")
        )
        stix_objects.append(
            dict_to_stix2(
                {
                    "type": "network-traffic",
                    "spec_version": "2.1",
                    "dst_ref": id,
                    "dst_port": port,
                    "protocols": ["ipv6"],
                }
            )
        )

    if stix_mapping == "domain-name":
        indicator["name"] = f"Domain: {value}"
        indicator["pattern"] = f"[ domain-name:value = { repr(value) } ]"

        stix_objects.append(
            dict_to_stix2(
                {"type": "domain-name", "spec_version": "2.1", "value": value}
            )
        )
        stix_objects.append(
            bundler.new_relationship(stix_objects[1].id, indicator["id"], "related-to")
        )

    if stix_mapping == "url":
        indicator["name"] = f"URL: {value}"
        indicator["pattern"] = f"[ url:value = { repr(value) } ]"

        stix_objects.append(
            dict_to_stix2({"type": "url", "spec_version": "2.1", "value": value})
        )
        stix_objects.append(
            bundler.new_relationship(stix_objects[1].id, indicator["id"], "related-to")
        )

    if stix_mapping == "file":
        indicator["name"] = f"File name: {value}"
        indicator["pattern"] = f"[ file:name = { repr(value) } ]"

        stix_objects.append(
            dict_to_stix2({"type": "file", "spec_version": "2.1", "name": value})
        )
        stix_objects.append(
            bundler.new_relationship(stix_objects[1].id, indicator["id"], "related-to")
        )

    if stix_mapping == "directory":
        indicator["name"] = f"Directory: {value}"
        indicator["pattern"] = f"[ directory:path = { repr(value) } ]"

        stix_objects.append(
            dict_to_stix2({"type": "directory", "spec_version": "2.1", "path": value})
        )
        stix_objects.append(
            bundler.new_relationship(stix_objects[1].id, indicator["id"], "related-to")
        )

    if stix_mapping == "directory-file":
        path = parse_path(value)
        value = str(path.parent)
        indicator["name"] = f"Directory: {value}"
        indicator["pattern"] = f"[ directory:path = { repr(value) } ]"

        stix_objects.append(
            dict_to_stix2({"type": "directory", "spec_version": "2.1", "path": value})
        )
        dir = stix_objects[-1]
        stix_objects.append(
            bundler.new_relationship(stix_objects[1].id, indicator["id"], "related-to")
        )

        stix_objects.append(
            dict_to_stix2({"type": "file", "spec_version": "2.1", "name": path.name})
        )
        file = stix_objects[-1]

        stix_objects.append(bundler.new_relationship(file.id, dir.id, "directory"))

    if stix_mapping == "file-hash":
        file_hash_type = find_hash_type(value, extractor.name) or extractor.slug
        # this needs to be updated, maybe puut hash_type in notes?
        indicator["name"] = f"{file_hash_type}: {value}"
        indicator["pattern"] = f"[ file:hashes.'{file_hash_type}' = { repr(value) } ]"
        stix_objects[0] = dict_to_stix2(indicator, allow_custom=True)

        stix_objects.append(
            dict_to_stix2(
                {
                    "type": "file",
                    "spec_version": "2.1",
                    "hashes": {file_hash_type: value},
                },
                allow_custom=True,
            )
        )
        stix_objects.append(
            bundler.new_relationship(stix_objects[1].id, indicator["id"], "related-to")
        )

    if stix_mapping == "email-addr":
        indicator["name"] = f"Email Address: {value}"
        indicator["pattern"] = f"[ email-addr:value = { repr(value) } ]"

        stix_objects.append(
            dict_to_stix2({"type": "email-addr", "spec_version": "2.1", "value": value})
        )
        stix_objects.append(
            bundler.new_relationship(stix_objects[1].id, indicator["id"], "related-to")
        )

    if stix_mapping == "mac-addr":
        indicator["name"] = f"MAC Address: {value}"
        indicator["pattern"] = f"[ mac-addr:value = { repr(value) } ]"

        stix_objects.append(
            dict_to_stix2({"type": "mac-addr", "spec_version": "2.1", "value": value})
        )
        stix_objects.append(
            bundler.new_relationship(stix_objects[1].id, indicator["id"], "related-to")
        )

    if stix_mapping == "windows-registry-key":
        indicator["name"] = f"Windows Registry Key: {value}"
        indicator["pattern"] = f"[ windows-registry-key:key = { repr(value) } ]"

        stix_objects.append(
            dict_to_stix2(
                {"type": "windows-registry-key", "spec_version": "2.1", "key": value}
            )
        )
        stix_objects.append(
            bundler.new_relationship(stix_objects[1].id, indicator["id"], "related-to")
        )

    if stix_mapping == "user-agent":
        indicator["name"] = f"User Agent: {value}"
        indicator["pattern"] = f"[ user-agent:string = { repr(value) } ]"

        stix_objects.append(
            dict_to_stix2(
                {"type": "user-agent", "spec_version": "2.1", "string": value}
            )
        )
        stix_objects.append(
            bundler.new_relationship(stix_objects[1].id, indicator["id"], "related-to")
        )

    if stix_mapping == "autonomous-system":
        match = re.search(r"\d+", value)
        if not match:
            raise MinorExcption(f"AS Number must contain a number, got `{value}`")
        value = match.group(0)
        indicator["name"] = f"AS{value}"
        indicator["pattern"] = f"[ autonomous-system:number = { repr(value) } ]"

        stix_objects.append(
            dict_to_stix2(
                {"type": "autonomous-system", "spec_version": "2.1", "number": value}
            )
        )
        stix_objects.append(
            bundler.new_relationship(stix_objects[1].id, indicator["id"], "related-to")
        )

    if stix_mapping == "cryptocurrency-wallet":
        # ASSUMPTION: always BTC
        # TODO: parse crypto types

        currency_symbol = "BTC"
        btc2stix = crypto2stix.BTC2Stix()
        indicator["name"] = f"{currency_symbol} Wallet: {value}"
        indicator["pattern"] = f"[ cryptocurrency-wallet:address = { repr(value) } ]"
        wallet_obj, *other_objects = btc2stix.process_wallet(value, wallet_only=True, transactions_only=False)

        stix_objects.append(
            wallet_obj
        )
        stix_objects.extend(other_objects)
        stix_objects.append(
            bundler.new_relationship(wallet_obj.id, indicator["id"], "related-to")
        )
        return stix_objects, [wallet_obj.id]

    if stix_mapping == "cryptocurrency-transaction":
        # ASSUMPTION: always BTC
        # TODO: do something about this
        currency_symbol = "BTC"
        btc2stix = crypto2stix.BTC2Stix()
        txn_object, *other_objects = btc2stix.process_transaction(value)
        indicator["name"] = f"{currency_symbol} Transaction: {value}"
        indicator["pattern"] = f"[ cryptocurrency-transaction:hash = { repr(value) } ]"

        stix_objects.append(
            txn_object
        )
        stix_objects.extend(other_objects)
        stix_objects.append(
            bundler.new_relationship(txn_object.id, indicator["id"], "related-to")
        )

        return stix_objects, [txn_object.id]

    if stix_mapping == "bank-card":
        # TODO
        card_type = extractor.name
        if "Bank Card" in extractor.name:
            card_type = extractor.name.split("Bank Card ")[1]

        value = value.replace("-", "").replace(" ", "")
        card_object, *other_objects = creditcard2stix.create_objects({'card_number': value}, os.getenv("BIN_LIST_API_KEY", ""))
        stix_objects.append(card_object)
        stix_objects.extend(other_objects)

        if  card_object.get('scheme'):
            card_type = card_object['scheme']

        indicator["name"] = f"{card_type}: {value}"
        indicator["pattern"] = f"[ bank-card:number = { repr(value) } ]"

        stix_objects.append(
            bundler.new_relationship(card_object['id'], indicator["id"], "related-to")
        )
        return stix_objects, [card_object['id']]

    if stix_mapping == "bank-account":
        indicator["name"] = f"Bank account: {value}"
        indicator["pattern"] = f"[ bank-account:iban_number = { repr(value) } ]"
        value = value.replace("-", "").replace(" ", "")

        country_code, bank_code = get_iban_details(value)

        stix_objects.append(
            dict_to_stix2(
                {
                    "type": "bank-account",
                    "spec_version": "2.1",
                    "iban_number": value,
                    "country": country_code,
                }
            )
        )
        stix_objects.append(
            bundler.new_relationship(stix_objects[1].id, indicator["id"], "related-to")
        )

    if stix_mapping == "phone-number":
        country_code = get_country_code(value)
        indicator["name"] = f"Phone Number: {value}"
        indicator["pattern"] = f"[ phone-number:number = { repr(value) }"
        if country_code:
            indicator["pattern"] += f" AND phone-number:country = '{country_code}' "
        indicator["pattern"] += " ]"

        stix_objects.append(
            dict_to_stix2(
                {
                    "type": "phone-number",
                    "spec_version": "2.1",
                    "number": value,
                    "country": country_code,
                }
            )
        )
        stix_objects.append(
            bundler.new_relationship(stix_objects[1].id, indicator["id"], "related-to")
        )

    if stix_mapping == "attack-pattern":
        stix_objects = [
            dict_to_stix2(
                {
                    "type": "attack-pattern",
                    "spec_version": "2.1",
                    "created_by_ref": indicator["created_by_ref"],
                    "created": indicator["created"],
                    "modified": indicator["modified"],
                    "name": value,
                    "external_references": indicator["external_references"],
                }
            )
        ]

    if stix_mapping == "campaign":
        stix_objects = [
            dict_to_stix2(
                {
                    "type": "campaign",
                    "spec_version": "2.1",
                    "created_by_ref": indicator["created_by_ref"],
                    "created": indicator["created"],
                    "modified": indicator["modified"],
                    "name": value,
                    "object_marking_refs": indicator["object_marking_refs"],
                    "external_references": indicator["external_references"],
                }
            )
        ]

    if stix_mapping == "course-of-action":
        stix_objects = [
            dict_to_stix2(
                {
                    "type": "course-of-action",
                    "spec_version": "2.1",
                    "created_by_ref": indicator["created_by_ref"],
                    "created": indicator["created"],
                    "modified": indicator["modified"],
                    "name": value,
                    "object_marking_refs": indicator["object_marking_refs"],
                    "external_references": indicator["external_references"],
                }
            )
        ]

    if stix_mapping == "infrastructure":
        stix_objects = [
            dict_to_stix2(
                {
                    "type": "infrastructure",
                    "spec_version": "2.1",
                    "created_by_ref": indicator["created_by_ref"],
                    "created": indicator["created"],
                    "modified": indicator["modified"],
                    "name": value,
                    "infrastructure_types": ["unknown"],
                    "object_marking_refs": indicator["object_marking_refs"],
                    "external_references": indicator["external_references"],
                }
            )
        ]

    if stix_mapping == "intrusion-set":
        stix_objects = [
            (
                dict_to_stix2(
                    {
                        "type": "intrusion-set",
                        "spec_version": "2.1",
                        "created_by_ref": indicator["created_by_ref"],
                        "created": indicator["created"],
                        "modified": indicator["modified"],
                        "name": value,
                        "object_marking_refs": indicator["object_marking_refs"],
                        "external_references": indicator["external_references"],
                    }
                )
            )
        ]

    if stix_mapping == "malware":
        stix_objects = [
            dict_to_stix2(
                {
                    "type": "malware",
                    "spec_version": "2.1",
                    "created_by_ref": indicator["created_by_ref"],
                    "created": indicator["created"],
                    "modified": indicator["modified"],
                    "name": value,
                    "malware_types": ["unknown"],
                    "is_family": True,
                    "object_marking_refs": indicator["object_marking_refs"],
                    "external_references": indicator["external_references"],
                }
            )
        ]

    if stix_mapping == "threat-actor":
        stix_objects = [
            dict_to_stix2(
                {
                    "type": "threat-actor",
                    "spec_version": "2.1",
                    "created_by_ref": indicator["created_by_ref"],
                    "created": indicator["created"],
                    "modified": indicator["modified"],
                    "name": value,
                    "threat_actor_types": "unknown",
                    "object_marking_refs": indicator["object_marking_refs"],
                    "external_references": indicator["external_references"],
                }
            )
        ]

    if stix_mapping == "tool":
        stix_objects = [
            dict_to_stix2(
                {
                    "type": "tool",
                    "spec_version": "2.1",
                    "created_by_ref": indicator["created_by_ref"],
                    "created": indicator["created"],
                    "modified": indicator["modified"],
                    "name": value,
                    "tool_types": "unknown",
                    "object_marking_refs": indicator["object_marking_refs"],
                    "external_references": indicator["external_references"],
                }
            )
        ]

    if stix_mapping == "identity":
        stix_objects = [
            dict_to_stix2(
                {
                    "type": "identity",
                    "spec_version": "2.1",
                    "created_by_ref": indicator["created_by_ref"],
                    "created": indicator["created"],
                    "modified": indicator["modified"],
                    "name": value,
                    "identity_class": "unspecified",
                    "object_marking_refs": indicator["object_marking_refs"],
                    "external_references": indicator["external_references"],
                }
            )
        ]

    if stix_mapping == "location":
        stix_objects.append(
            dict_to_stix2(
                {
                    "type": "location",
                    "spec_version": "2.1",
                    "created_by_ref": indicator["created_by_ref"],
                    "created": indicator["created"],
                    "modified": indicator["modified"],
                    "name": f"Country: {value}",
                    "country": value,
                    "object_marking_refs": indicator["object_marking_refs"],
                    "external_references": indicator["external_references"],
                }
            )
        )
        stix_objects.append(
            bundler.new_relationship(stix_objects[1].id, indicator["id"], "related-to")
        )

    RELATABLE = [
        "ipv4-addr",
        "ipv4-addr",
        "ipv6-addr",
        "ipv6-addr",
        "domain-name",
        "url",
        "file",
        "directory",
        "directory",
        "file",
        "email-addr",
        "mac-addr",
        "windows-registry-key",
        "autonomous-system",
        "user-agent",
        "cryptocurrency-wallet",
        "cryptocurrency-transaction",
        "bank-card",
        "bank-card",
        "phone-number",
        "attack-pattern",
        "campaign",
        "course-of-action",
        "infrastructure",
        "intrusion-set",
        "malware",
        "threat-actor",
        "tool",
        "identity",
        "location",
    ]
    relationships = []
    for i, indicator in enumerate(stix_objects):
        if isinstance(indicator, dict):
            indicator = dict_to_stix2(indicator)
            stix_objects[i] = indicator
        if indicator.type in RELATABLE:
            relationships.append(indicator.id)

    return stix_objects, relationships


def arangodb_check(stix_mapping, id):
    try:
        s = ArangoSession()
        if stix_mapping in s.ATTACK_ID_TABLES:
            return s.mitre_attack_id(id, stix_mapping)
        if stix_mapping == "mitre-capec-id":
            return s.mitre_capec_id(id)
        if stix_mapping == "mitre-cwe-id":
            return s.mitre_cwe_id(id)
        if stix_mapping == "cve-id":
            return s.cve_id(id)
        if stix_mapping == "cpe-id":
            return s.cpe_id(id)
    except Exception as e:
        pass
    return None


# print(build_indicator("ipv4-addr", {}, "192.168.0.1"))
# print(build_indicator("ipv4-addr-port", {}, "192.168.0.1:80"))
# print(build_indicator("cryptocurrency-wallet", {}, "192.168.0.1:80"))
# print(get_country_code("2349027338509"))
