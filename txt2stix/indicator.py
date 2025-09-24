from __future__ import annotations
import os
import re
from stix2.parsing import dict_to_stix2
from stix2 import HashConstant
from stix2.v21.vocab import HASHING_ALGORITHM
from stix2.patterns import _HASH_REGEX as HASHING_ALGORITHM_2
from ipaddress import ip_address
from pathlib import PurePosixPath, PureWindowsPath
from phonenumbers import geocoder
import logging
from stix2extensions.tools import creditcard2stix, crypto2stix
from typing import TYPE_CHECKING

import validators

from txt2stix.pattern.extractors.others.phonenumber_extractor import PhoneNumberExtractor
from txt2stix.utils import validate_file_mimetype, validate_reg_key

if TYPE_CHECKING:
    from .bundler import txt2stixBundler

# from schwifty import IBAN

from .common import MinorException

from .retriever import retrieve_stix_objects

logger = logging.getLogger("txt2stix.indicator")


class BadDataException(MinorException):
    pass


def validate_email(email_addr):
    _, domain_part = email_addr.rsplit("@", 1)
    return validators.domain(domain_part, consider_tld=True) and validators.email(
        email_addr
    )


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
        path = PurePosixPath(pathstr)
    return path


def split_ip_port(ip_port: str):
    ip, _, port = ip_port.rpartition(":")
    ip = ip.replace("[", "").replace("]", "")  # remove the [] enclosuure if it's ipv6
    ip = ip_address(ip)

    return ip.exploded, int(port)

def get_country_code(number: str) -> str:
    phone = PhoneNumberExtractor.parse_phone_number(number)
    if phone:
        return geocoder.region_codes_for_country_code(phone.country_code)[0]
    else:
        raise BadDataException('bad phone number')


def get_iban_details(number) -> tuple[str, str]:
    return number[:2], None


def build_observables(
    bundler: txt2stixBundler, stix_mapping, indicator, extracted_value, extractor
):
    try:
        return _build_observables(
            bundler, stix_mapping, indicator, extracted_value, extractor
        )
    except BadDataException:
        raise
    except BaseException as e:
        raise BadDataException("unknown data error") from e


def _build_observables(
    bundler: txt2stixBundler, stix_mapping, indicator, extracted_value, extractor
):
    retrieved_objects = retrieve_stix_objects(stix_mapping, extracted_value)
    if retrieved_objects:
        return retrieved_objects, [sdo["id"] for sdo in retrieved_objects]
    if retrieved_objects == []:
        logger.warning(
            f"could not find `{stix_mapping}` with id=`{extracted_value}` in remote"
        )
        raise BadDataException(
            f"could not find `{stix_mapping}` with id=`{extracted_value}` in remote"
        )

    stix_objects = [indicator]

    if stix_mapping == "ipv4-addr":
        indicator["name"] = f"ipv4: {extracted_value}"
        indicator["pattern"] = f"[ ipv4-addr:value = { repr(extracted_value) } ]"

        stix_objects.append(
            dict_to_stix2(
                {"type": "ipv4-addr", "spec_version": "2.1", "value": extracted_value}
            )
        )

        stix_objects.append(
            bundler.new_relationship(
                stix_objects[1].id,
                indicator["id"],
                "detected-using",
                description=f"{stix_objects[1]['value']} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
        )

    if stix_mapping == "ipv4-addr-port":
        extracted_value, port = split_ip_port(extracted_value)
        indicator["name"] = f"ipv4: {extracted_value}"
        indicator["pattern"] = f"[ ipv4-addr:value = { repr(extracted_value) } ]"

        stix_objects.append(
            dict_to_stix2(
                {"type": "ipv4-addr", "spec_version": "2.1", "value": extracted_value}
            )
        )
        id = stix_objects[-1].id
        stix_objects.append(
            bundler.new_relationship(
                stix_objects[1].id,
                indicator["id"],
                "detected-using",
                description=f"{stix_objects[1]['value']} can be detected in the STIX pattern {indicator['name']}",
            )
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
        indicator["name"] = f"ipv6: {extracted_value}"
        indicator["pattern"] = f"[ ipv6-addr:value = { repr(extracted_value) } ]"

        stix_objects.append(
            dict_to_stix2(
                {"type": "ipv6-addr", "spec_version": "2.1", "value": extracted_value}
            )
        )
        stix_objects.append(
            bundler.new_relationship(
                stix_objects[1].id,
                indicator["id"],
                "detected-using",
                description=f"{stix_objects[1]['value']} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
        )

    if stix_mapping == "ipv6-addr-port":
        extracted_value, port = split_ip_port(extracted_value)
        indicator["name"] = f"ipv6: {extracted_value}"
        indicator["pattern"] = f"[ ipv6-addr:value = { repr(extracted_value) } ]"

        stix_objects.append(
            dict_to_stix2(
                {"type": "ipv6-addr", "spec_version": "2.1", "value": extracted_value}
            )
        )
        id = stix_objects[-1].id
        stix_objects.append(
            bundler.new_relationship(
                stix_objects[1].id,
                indicator["id"],
                "detected-using",
                description=f"{stix_objects[1]['value']} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
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
        q = validators.hostname(
            extracted_value,
            may_have_port=False,
            skip_ipv6_addr=True,
            skip_ipv4_addr=True,
        )
        if q != True:
            r = validators.domain(extracted_value, consider_tld=True)
            if r != True:
                raise BadDataException("invalid domain or hostname") from r
        indicator["name"] = f"Domain: {extracted_value}"
        indicator["pattern"] = f"[ domain-name:value = { repr(extracted_value) } ]"

        stix_objects.append(
            dict_to_stix2(
                {"type": "domain-name", "spec_version": "2.1", "value": extracted_value}
            )
        )
        stix_objects.append(
            bundler.new_relationship(
                stix_objects[1].id,
                indicator["id"],
                "detected-using",
                description=f"{extracted_value} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
        )

    if stix_mapping == "url":
        if (q := validators.url(extracted_value, simple_host=True)) and q != True:
            raise BadDataException("invalid url") from q
        # assert validators.url(extracted_value) == True
        indicator["name"] = f"URL: {extracted_value}"
        indicator["pattern"] = f"[ url:value = { repr(extracted_value) } ]"

        stix_objects.append(
            dict_to_stix2(
                {"type": "url", "spec_version": "2.1", "value": extracted_value}
            )
        )
        stix_objects.append(
            bundler.new_relationship(
                stix_objects[1].id,
                indicator["id"],
                "detected-using",
                description=f"{extracted_value} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
        )

    mimetype = validate_file_mimetype(extracted_value)
    if stix_mapping in ["file", "directory-file"]:
        if not mimetype:
            raise BadDataException(f"invalid file extension in `{extracted_value}`")

    if stix_mapping == "file":
        file = dict_to_stix2(
            {
                "type": "file",
                "spec_version": "2.1",
                "name": extracted_value,
                "mime_type": mimetype,
            }
        )
        indicator["name"] = f"File name: {extracted_value}"
        indicator["pattern"] = f"[ file:name = { repr(extracted_value) } ]"

        stix_objects.append(file)
        stix_objects.append(
            bundler.new_relationship(
                stix_objects[1].id,
                indicator["id"],
                "detected-using",
                description=f"{extracted_value} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
        )

    if stix_mapping == "directory":
        indicator["name"] = f"Directory: {extracted_value}"
        indicator["pattern"] = f"[ directory:path = { repr(extracted_value) } ]"

        stix_objects.append(
            dict_to_stix2(
                {"type": "directory", "spec_version": "2.1", "path": extracted_value}
            )
        )
        stix_objects.append(
            bundler.new_relationship(
                stix_objects[1].id,
                indicator["id"],
                "detected-using",
                description=f"{extracted_value} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
        )

    if stix_mapping == "directory-file":
        path = parse_path(extracted_value)
        dir_obj = dict_to_stix2(
            {"type": "directory", "spec_version": "2.1", "path": str(path.parent)}
        )
        file = dict_to_stix2(
            {
                "type": "file",
                "spec_version": "2.1",
                "name": path.name,
                "mime_type": mimetype,
                "parent_directory_ref": dir_obj.id,
            }
        )
        indicator["name"] = f"Directory File: {extracted_value}"
        indicator["pattern"] = f"[ directory:path = { repr(dir_obj.path) }  OR file:name = {repr(file.name)}]"

        stix_objects.append(dir_obj)
        stix_objects.append(file)
        stix_objects.append(
            bundler.new_relationship(
                file.id,
                indicator["id"],
                "detected-using",
                description=f"{extracted_value} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
        )
        return stix_objects, [file.id]

    if stix_mapping == "file-hash":
        file_hash_type = (
            find_hash_type(extracted_value, extractor.name) or extractor.slug
        )
        # this needs to be updated, maybe put hash_type in notes?
        indicator["name"] = f"{file_hash_type}: {extracted_value}"
        indicator["pattern"] = (
            f"[ file:hashes.'{file_hash_type}' = { repr(extracted_value) } ]"
        )
        stix_objects[0] = dict_to_stix2(indicator, allow_custom=True)

        stix_objects.append(
            dict_to_stix2(
                {
                    "type": "file",
                    "spec_version": "2.1",
                    "hashes": {file_hash_type: extracted_value},
                },
                allow_custom=True,
            )
        )
        stix_objects.append(
            bundler.new_relationship(
                stix_objects[1].id,
                indicator["id"],
                "detected-using",
                description=f"{extracted_value} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
        )

    if stix_mapping == "email-addr":
        q = validate_email(extracted_value)
        if q != True:
            raise BadDataException("invalid email") from q
        indicator["name"] = f"Email Address: {extracted_value}"
        indicator["pattern"] = f"[ email-addr:value = { repr(extracted_value) } ]"

        stix_objects.append(
            dict_to_stix2(
                {"type": "email-addr", "spec_version": "2.1", "value": extracted_value}
            )
        )
        stix_objects.append(
            bundler.new_relationship(
                stix_objects[1].id,
                indicator["id"],
                "detected-using",
                description=f"{extracted_value} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
        )

    if stix_mapping == "mac-addr":
        q = validators.mac_address(extracted_value)
        if q != True:
            raise BadDataException("invalid email") from q
        indicator["name"] = f"MAC Address: {extracted_value}"
        indicator["pattern"] = f"[ mac-addr:value = { repr(extracted_value) } ]"

        stix_objects.append(
            dict_to_stix2(
                {"type": "mac-addr", "spec_version": "2.1", "value": extracted_value}
            )
        )
        stix_objects.append(
            bundler.new_relationship(
                stix_objects[1].id,
                indicator["id"],
                "detected-using",
                description=f"{extracted_value} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
        )

    if stix_mapping == "windows-registry-key":
        if not validate_reg_key(extracted_value):
            raise BadDataException("Invalid registry key")
        indicator["name"] = f"Windows Registry Key: {extracted_value}"
        indicator["pattern"] = (
            f"[ windows-registry-key:key = { repr(extracted_value) } ]"
        )

        stix_objects.append(
            dict_to_stix2(
                {
                    "type": "windows-registry-key",
                    "spec_version": "2.1",
                    "key": extracted_value,
                }
            )
        )
        stix_objects.append(
            bundler.new_relationship(
                stix_objects[1].id,
                indicator["id"],
                "detected-using",
                description=f"{extracted_value} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
        )

    if stix_mapping == "user-agent":
        indicator["name"] = f"User Agent: {extracted_value}"
        indicator["pattern"] = f"[ user-agent:string = { repr(extracted_value) } ]"

        stix_objects.append(
            dict_to_stix2(
                {"type": "user-agent", "spec_version": "2.1", "string": extracted_value}
            )
        )
        stix_objects.append(
            bundler.new_relationship(
                stix_objects[1].id,
                indicator["id"],
                "detected-using",
                description=f"{extracted_value} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
        )

    if stix_mapping == "autonomous-system":
        match = re.search(r"\d+", extracted_value)
        if not match:
            raise BadDataException(
                f"AS Number must contain a number, got `{extracted_value}`"
            )
        extracted_value = int(match.group(0))
        assert extracted_value >= 1 and extracted_value <= 65535, "AS Number must be between 1 and 65535"
        indicator["name"] = f"AS{extracted_value}"
        indicator["pattern"] = (
            f"[ autonomous-system:number = { repr(extracted_value) } ]"
        )

        stix_objects.append(
            dict_to_stix2(
                {
                    "type": "autonomous-system",
                    "spec_version": "2.1",
                    "number": extracted_value,
                }
            )
        )
        stix_objects.append(
            bundler.new_relationship(
                stix_objects[1].id,
                indicator["id"],
                "detected-using",
                description=f"{extracted_value} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
        )

    if stix_mapping == "cryptocurrency-wallet":
        # ASSUMPTION: always BTC
        # TODO: parse crypto types

        currency_symbol = "BTC"
        btc2stix = crypto2stix.BTC2Stix()
        indicator["name"] = f"{currency_symbol} Wallet: {extracted_value}"
        indicator["pattern"] = (
            f"[ cryptocurrency-wallet:address = { repr(extracted_value) } ]"
        )
        wallet_obj, *other_objects = btc2stix.process_wallet(
            extracted_value, wallet_only=True, transactions_only=False
        )

        stix_objects.append(wallet_obj)
        stix_objects.extend(other_objects)
        stix_objects.append(
            bundler.new_relationship(
                wallet_obj.id,
                indicator["id"],
                "detected-using",
                description=f"{extracted_value} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
        )
        return stix_objects, [wallet_obj.id]

    if stix_mapping == "cryptocurrency-transaction":
        # ASSUMPTION: always BTC
        # TODO: do something about this
        currency_symbol = "BTC"
        btc2stix = crypto2stix.BTC2Stix()
        txn_object, *other_objects = btc2stix.process_transaction(extracted_value)
        indicator["name"] = f"{currency_symbol} Transaction: {extracted_value}"
        indicator["pattern"] = (
            f"[ cryptocurrency-transaction:hash = { repr(extracted_value) } ]"
        )

        stix_objects.append(txn_object)
        stix_objects.extend(other_objects)
        stix_objects.append(
            bundler.new_relationship(
                txn_object.id,
                indicator["id"],
                "detected-using",
                description=f"{extracted_value} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
        )

        return stix_objects, [txn_object.id]

    if stix_mapping == "cryptocurrency-wallet-with-transaction":
        # ASSUMPTION: always BTC
        # TODO: parse crypto types

        currency_symbol = "BTC"
        btc2stix = crypto2stix.BTC2Stix()
        indicator["name"] = f"{currency_symbol} Wallet: {extracted_value}"
        indicator["pattern"] = (
            f"[ cryptocurrency-wallet:address = { repr(extracted_value) } ]"
        )
        wallet_obj, *other_objects = btc2stix.process_wallet(
            extracted_value, wallet_only=False, transactions_only=True
        )

        stix_objects.append(wallet_obj)
        stix_objects.extend(other_objects)
        stix_objects.append(
            bundler.new_relationship(
                wallet_obj.id,
                indicator["id"],
                "detected-using",
                description=f"{extracted_value} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
        )
        return stix_objects, [wallet_obj.id]
    if stix_mapping == "bank-card":
        # TODO
        card_type = extractor.name
        if "Bank Card" in extractor.name:
            card_type = extractor.name.split("Bank Card ")[1]

        extracted_value = extracted_value.replace("-", "").replace(" ", "")
        indicator["id"] = bundler.indicator_id_from_value(extracted_value, stix_mapping)
        card_object, *other_objects = creditcard2stix.create_objects(
            {"card_number": extracted_value}, os.getenv("BIN_LIST_API_KEY", "")
        )
        stix_objects.append(card_object)
        stix_objects.extend(other_objects)

        if card_object.get("scheme"):
            card_type = card_object["scheme"]

        indicator["name"] = f"{card_type}: {extracted_value}"
        indicator["pattern"] = f"[ bank-card:number = { repr(extracted_value) } ]"

        stix_objects.append(
            bundler.new_relationship(
                card_object["id"],
                indicator["id"],
                "detected-using",
                description=f"{extracted_value} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
        )
        return stix_objects, [card_object["id"]]

    if stix_mapping == "bank-account":
        q = validators.iban(extracted_value)
        if q != True:
            raise BadDataException('invalid iban number') from q
        indicator["name"] = f"Bank account: {extracted_value}"
        indicator["pattern"] = (
            f"[ bank-account:iban_number = { repr(extracted_value) } ]"
        )
        extracted_value = extracted_value.replace("-", "").replace(" ", "")

        country_code, bank_code = get_iban_details(extracted_value)

        stix_objects.append(
            dict_to_stix2(
                {
                    "type": "bank-account",
                    "spec_version": "2.1",
                    "iban_number": extracted_value,
                    "country": country_code,
                }
            )
        )
        stix_objects.append(
            bundler.new_relationship(
                stix_objects[1].id,
                indicator["id"],
                "detected-using",
                description=f"{extracted_value} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
        )

    if stix_mapping == "phone-number":
        country_code = get_country_code(extracted_value)
        if not country_code:
            raise BadDataException('parse phone number failed')
        indicator["name"] = f"Phone Number: {extracted_value}"
        indicator["pattern"] = f"[ phone-number:number = { repr(extracted_value) }"
        if country_code:
            indicator["pattern"] += f" AND phone-number:country = '{country_code}' "
        indicator["pattern"] += " ]"

        stix_objects.append(
            dict_to_stix2(
                {
                    "type": "phone-number",
                    "spec_version": "2.1",
                    "number": extracted_value,
                    "country": country_code,
                }
            )
        )
        stix_objects.append(
            bundler.new_relationship(
                stix_objects[1].id,
                indicator["id"],
                "detected-using",
                description=f"{extracted_value} can be detected in the STIX pattern {indicator['name']}",
                external_references=indicator["external_references"],
            )
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
                    "name": extracted_value,
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
                    "name": extracted_value,
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
                    "name": extracted_value,
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
                    "name": extracted_value,
                    "infrastructure_types": ["unknown"],
                    "object_marking_refs": indicator["object_marking_refs"],
                    "external_references": indicator["external_references"],
                }
            )
        ]

    if stix_mapping == "intrusion-set":
        stix_objects = [
            dict_to_stix2(
                {
                    "type": "intrusion-set",
                    "spec_version": "2.1",
                    "created_by_ref": indicator["created_by_ref"],
                    "created": indicator["created"],
                    "modified": indicator["modified"],
                    "name": extracted_value,
                    "object_marking_refs": indicator["object_marking_refs"],
                    "external_references": indicator["external_references"],
                }
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
                    "name": extracted_value,
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
                    "name": extracted_value,
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
                    "name": extracted_value,
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
                    "name": extracted_value,
                    "identity_class": "unspecified",
                    "object_marking_refs": indicator["object_marking_refs"],
                    "external_references": indicator["external_references"],
                }
            )
        ]

    RELATABLE = [
        "ipv4-addr",
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
        "bank-account",
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
