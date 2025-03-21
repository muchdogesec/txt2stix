from pathlib import PurePosixPath, PureWindowsPath
import pytest
from unittest import mock
from txt2stix import get_all_extractors
from txt2stix.indicator import (
    build_observables,
    find_hash_type,
    parse_path,
    split_ip_port,
    get_country_code,
    get_iban_details,
    BadDataException,
)
from stix2 import HashConstant

from txt2stix.stix import txt2stixBundler
from datetime import datetime


def test_find_hash_type_with_valid_hash_algorithm():
    value = "dummy_value"
    name = "SHA-256"
    result = find_hash_type(value, name)
    assert result == "SHA-256"


def test_find_hash_type_with_invalid_algorithm():
    value = "dummy_value"
    name = "INVALID_HASH"
    result = find_hash_type(value, name)
    assert result is None


@mock.patch("stix2.HashConstant")
def test_find_hash_type_with_valid_hash_using_hash_constant(mock_hash_constant):
    value = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    name = "SHA-256"
    mock_hash_constant.return_value = HashConstant(value, name)
    result = find_hash_type(value, name)
    assert result == "SHA-256"


# Tests for parse_path function
def test_parse_path_with_windows_path():
    pathstr = "C:\\Users\\Test\\Documents"
    result = parse_path(pathstr)
    assert result == PureWindowsPath(pathstr)


def test_parse_path_with_posix_path():
    pathstr = "/home/user/test"
    result = parse_path(pathstr)
    assert result == PurePosixPath(pathstr)


@pytest.mark.parametrize(
    ["ip_port", "ip", "port"],
    [
        ("192.168.1.1:8001", "192.168.1.1", 8001),
        (
            "[2001:0db8:85a3:0000:0000:8a2e:0370:7334]:8080",
            "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
            8080,
        ),
    ],
)
def test_split_ip_port_ipv4(ip_port, ip, port):
    assert split_ip_port(ip_port) == (ip, port)


@pytest.mark.parametrize(
    ["number", "country"],
    [
        ("+14155552671", "US"),
        ("+864155552671", "CN"),
        ("+2349012345678", "NG"),
    ],
)
def test_get_country_code_valid_number(number, country):
    assert get_country_code(number) == country


@pytest.mark.parametrize(
    ["iban", "country"],
    [
        ("GB29NWBK60161331926819", "GB"),
        ("INVALIDIBAN", "IN"),
    ],
)
def test_get_iban_details_valid_iban(iban, country):
    country_code, _ = get_iban_details(iban)
    assert country_code == country


mock_bundler = txt2stixBundler(
    name="test_indicator.py",
    identity=None,
    tlp_level="red",
    description="",
    confidence=None,
    extractors=None,
    labels=None,
    created=datetime(2020, 1, 1),
)
all_extractors = get_all_extractors()


@pytest.mark.parametrize(
    ["value", "extractor_name", "expected_objects", "expected_rels"],
    [
        ### ipv4
        [
            "127.0.0.1",
            "pattern_ipv4_address_only",
            {
                "ipv4-addr--679c6c82-b4be-52e2-9c7a-198689f6f77b",
                "indicator--e2fdd3e3-f28f-5429-844f-6f7ee6e33354",
                "relationship--f0fc8f9b-6bf8-5d68-9dd2-0894de179346",
            },
            {"ipv4-addr--679c6c82-b4be-52e2-9c7a-198689f6f77b"},
        ],
        [
            "127.0.0.1:8080",
            "pattern_ipv4_address_port",
            {
                "ipv4-addr--679c6c82-b4be-52e2-9c7a-198689f6f77b",
                "indicator--50bf1229-1886-527b-830e-b4decaca8fff",
                "relationship--54f4d24a-e819-5f07-82ce-3e768aed3ebf",
                "network-traffic--bc4336c7-af88-5853-a21b-f319938f9aac",
            },
            {"ipv4-addr--679c6c82-b4be-52e2-9c7a-198689f6f77b"},
        ],
        [
            "127.0.0.1/16",
            "pattern_ipv4_address_cidr",
            {
                "ipv4-addr--31e0d7f3-97af-5dce-a98a-d9f7a06ea485",
                "relationship--742fc563-499f-52a3-9021-6ef12b96e676",
                "indicator--9a5c317c-69b9-5264-9be2-c2565cfc89f3",
            },
            {"ipv4-addr--31e0d7f3-97af-5dce-a98a-d9f7a06ea485"},
        ],
        ### ipv6
        [
            "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
            "pattern_ipv6_address_only",
            {
                "indicator--2d2c0ef2-27db-5be0-be0d-519bc626991b",
                "relationship--a1c3c9cd-0194-5158-8612-fb4bd6ad8f55",
                "ipv6-addr--85a85a8c-ee99-5722-946d-3c3a3270fc6f",
            },
            {"ipv6-addr--85a85a8c-ee99-5722-946d-3c3a3270fc6f"},
        ],
        [
            "[2001:0db8:85a3:0000:0000:8a2e:0370:7334]:8080",
            "pattern_ipv6_address_port",
            {
                "ipv6-addr--85a85a8c-ee99-5722-946d-3c3a3270fc6f",
                "network-traffic--d7f1aefc-12ba-53d6-a2c8-c54d7b956e39",
                "indicator--90651196-ef6c-5d37-88dc-f3ec8d086139",
                "relationship--1a92e99f-8ba1-5623-8c0a-f04901019789",
            },
            {"ipv6-addr--85a85a8c-ee99-5722-946d-3c3a3270fc6f"},
        ],
        ## domain-name
        [
            "localhost",
            "pattern_host_name",
            [
                "indicator--b191e1b9-6557-5aaf-aa67-101513a1c262",
                "domain-name--b54e23fc-08b6-5d8e-b593-bf0dfc0a49d5",
                "relationship--fb949e5a-1aca-504b-9f1e-9b771c3bd1b3",
            ],
            [
                "domain-name--b54e23fc-08b6-5d8e-b593-bf0dfc0a49d5",
            ],
        ],
        [
            "somewebsite.gg",
            "pattern_host_name",
            [
                "indicator--3438c8cc-d5be-5a10-90d5-fc016f8d5dcb",
                "relationship--d9f1c8c6-79b7-5afd-af5c-04f38452eb21",
                "domain-name--6b8b0382-6675-5d04-8442-5a1e2d9e903f",
            ],
            [
                "domain-name--6b8b0382-6675-5d04-8442-5a1e2d9e903f",
            ],
        ],
        ## url
        [
            "http://localhost:123/die",
            "pattern_url",
            [
                "relationship--e39bdd84-ebb3-5114-b8e5-25d2516ca4f9",
                "url--b427c195-2f31-55c4-a41e-ce2beb48cf01",
                "indicator--6cb54bc9-a7ed-546c-9ff7-28f67514228d",
            ],
            [
                "url--b427c195-2f31-55c4-a41e-ce2beb48cf01",
            ],
        ],
        ## file
        [
            "file.jpg",
            "pattern_file_name",
            [
                "indicator--02cef367-08f9-527c-ba46-bb31f1688f73",
                "relationship--99e465b0-bb35-5552-9131-c0c3dc301269",
                "file--a525dace-961b-5749-b9c3-3e2feba0034c",
            ],
            [
                "file--a525dace-961b-5749-b9c3-3e2feba0034c",
            ],
        ],
        ## directory-file
        [
            "/path/to/dir/die.exe",
            "pattern_directory_unix_file",
            [
                "relationship--53204f97-f4c3-59ca-9158-f0c973efd8d9",
                "file--7dbeff1a-48b6-5060-a637-04fa55f93c9a",
                "directory--1377fe61-b48b-5250-985b-db5ff7f97200",
                "relationship--83ff7176-d5eb-52a0-bd4d-abc2d63969d3",
                "indicator--af70d360-db9a-57c7-87c7-913db53fbdbb",
            ],
            [
                "directory--1377fe61-b48b-5250-985b-db5ff7f97200",
            ],
        ],
        ## file-hash
        [
            "86F7E437FAA5A7FCE15D1DDCB9EAEAEA377667B8",
            "pattern_file_hash_sha_1",
            {
                "indicator--cd379332-8625-5dac-a014-c756e36d7e8e",
                "file--109eb6b5-7257-568b-8a3a-146e343ac867",
                "relationship--c68979cd-f565-5881-bd8a-9e470abf64b9",
            },
            {
                "file--109eb6b5-7257-568b-8a3a-146e343ac867",
            },
        ],
        ## email-addr
        [
            "goo@gmail.com",
            "pattern_email_address",
            {
                "indicator--53e4ac19-8b6e-5af9-90a0-a0873ea6eadb",
                "email-addr--c582f4d4-bea6-5dec-951e-5b5e249f8fc5",
                "relationship--de1a930e-86ed-51f4-9073-cc940cd551df",
            },
            {
                "email-addr--c582f4d4-bea6-5dec-951e-5b5e249f8fc5",
            },
        ],
        ## mac-addr
        [
            "d2:fb:49:24:37:18",
            "pattern_mac_address",
            {
                "indicator--c6ee6505-d411-501d-89a3-32c516300245",
                "relationship--46174b25-21d5-5905-ac72-5293f523df51",
                "mac-addr--757b1725-9903-54f5-a855-1240691d7659",
            },
            {
                "mac-addr--757b1725-9903-54f5-a855-1240691d7659",
            },
        ],
        ## windows-registry-key
        [
            r"HKLM\Short\\Name",
            "pattern_windows_registry_key",
            {
                "indicator--f1ec43d2-3695-59dd-a56b-40fcf57b3ab4",
                "relationship--4a07d23d-13f7-50b2-a6f6-86bd9e4b774b",
                "windows-registry-key--3be35eea-0b2d-5316-8f7d-46daf6b5029e",
            },
            {
                "windows-registry-key--3be35eea-0b2d-5316-8f7d-46daf6b5029e",
            },
        ],
        ## autonomous-system
        [
            "ASN15139",
            "pattern_autonomous_system_number",
            {
                "relationship--88d47e95-9871-53a8-ad15-8ecd967b3973",
                "autonomous-system--3aa27478-50b5-5ab8-9da9-cdc12b657fff",
                "indicator--7d4fba9e-cd24-5c75-a0ee-65f8128d5f90",
            },
            {
                "autonomous-system--3aa27478-50b5-5ab8-9da9-cdc12b657fff",
            },
        ],
        ## user-agent
        [
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.6) Gecko/20040113",
            "pattern_user_agent",
            {
                "user-agent--b71ac3f9-2e75-5f59-ada4-71e8a2514ec3",
                "indicator--6f93a665-a15c-512a-b4fa-c774fd1338c4",
                "relationship--189db81b-52c3-5e76-95ec-8bf51dc34bde",
            },
            {
                "user-agent--b71ac3f9-2e75-5f59-ada4-71e8a2514ec3",
            },
        ],
        ## cryptocurrency-wallet
        [
            "3Cwgr2g7vsi1bXDUkpEnVoRLA9w4FZfC69",
            "pattern_cryptocurrency_btc_wallet",
            {
                "indicator--d202ac23-ed4c-5639-be04-e4cca4556185",
                "cryptocurrency-wallet--6e43ef66-8082-5552-80f2-95f5a44f60aa",
                "relationship--6cf35051-4d19-5b7d-a63d-ba0e7b2b46e2",
            },
            {
                "cryptocurrency-wallet--6e43ef66-8082-5552-80f2-95f5a44f60aa",
            },
        ],
        ## bank-account
        [
            "DE29100500001061045672",
            "pattern_iban_number",
            {
                "bank-account--4c1507ea-fdde-556b-87c9-f8ef702a0d8a",
                "indicator--ad568fa2-4589-5cf2-b586-a5430d356c88",
                "relationship--8fc1207b-9321-57ce-b73a-75d699fd10d7",
            },
            {
                "bank-account--4c1507ea-fdde-556b-87c9-f8ef702a0d8a",
            },
        ],
        ## phone-number
        [
            "+442083661177",
            "pattern_phone_number",
            {
                "phone-number--9c0e11b8-10e5-5384-96ae-b3fe7799eb5e",
                "relationship--bdf64ea4-408b-5dfe-818a-8455f8a9d07b",
                "indicator--f3e9e2ad-8cec-50d0-a085-14fbace10e6c",
            },
            {
                "phone-number--9c0e11b8-10e5-5384-96ae-b3fe7799eb5e",
            },
        ],
        ## bank-card
        [
            "376654224631002",
            "pattern_bank_card_amex",
            {
                "bank-card--e19f1547-2b5f-5f3d-82dc-817c7ba15405",
                "indicator--538fafbc-a2d0-5728-97d5-a464ce158b3a",
                "relationship--11811543-770e-5ee2-811c-57815d0d16a9",
                'identity--672e6dbb-e4a0-5b81-8035-c06a1961c796', #issuer_identity
            },
            {
                "bank-card--e19f1547-2b5f-5f3d-82dc-817c7ba15405",
            },
        ],
    ],
)
def test_build_observables(value, extractor_name, expected_objects, expected_rels):
    extractor = all_extractors[extractor_name]
    indicator = mock_bundler.new_indicator(extractor, extractor.stix_mapping, value)
    objects, relationships = build_observables(
        mock_bundler, extractor.stix_mapping, indicator, value, extractor
    )
    assert {obj["id"] for obj in objects} == set(expected_objects)
    assert {id for id in relationships} == set(expected_rels)


@pytest.mark.parametrize(
    "extractor_name",
    {
        v.test_cases: k
        for k, v in all_extractors.items()
        if (
            v.test_cases
            not in [
                "ai_country",
                "generic_cryptocurrency_btc_wallet",  # deferred until stix2extension#11
                "generic_cryptocurrency_btc_transaction",  # deferred until stix2extension#11
                "generic_cve_id",  # deferred until vulmatch is live
                "generic_cpe_uri",  # deferred until vulmatch is live
            ]
            and not v.test_cases.startswith("generic_bank")  # binapi not working
            and v.stix_mapping
            not in [
                "url",
                "domain-name",
                "ipv4-addr",
                "ipv6-addr",
                "directory",
                "directory-file",
                "user-agent",
            ]
            and not (
                # can't test in post
                v.test_cases.startswith("lookup")
                and not v.stix_mapping.startswith("ctibutler")
            )
        )
    }.values(),
)
def test_build_observables_with_extractor_cases(extractor_name, subtests):
    extractor = all_extractors[extractor_name]

    for value in extractor.prompt_positive_examples:
        indicator = mock_bundler.new_indicator(extractor, extractor.stix_mapping, value)
        with subtests.test(
            "test_positive_cases",
            extractor=extractor.slug,
            value=value,
            test_cases=extractor.test_cases,
        ):
            objects, rels = build_observables(
                mock_bundler, extractor.stix_mapping, indicator, value, extractor
            )
            assert objects, "positive test case must return objects"

    for value in extractor.prompt_negative_examples:
        indicator = mock_bundler.new_indicator(extractor, extractor.stix_mapping, value)
        with subtests.test(
            "test_negative_cases",
            extractor=extractor.slug,
            value=value,
            test_cases=extractor.test_cases,
        ):
            with pytest.raises(BadDataException):
                v = build_observables(
                    mock_bundler, extractor.stix_mapping, indicator, value, extractor
                )
                assert False, len(v[0])
