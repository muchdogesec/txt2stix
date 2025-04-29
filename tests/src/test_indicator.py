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
                "indicator--867868bf-5743-5494-a207-644b49dce3c0",
                "relationship--16416ddf-5bd9-5189-b767-a99b36ccf03d",
            },
            {"ipv4-addr--679c6c82-b4be-52e2-9c7a-198689f6f77b"},
        ],
        [
            "127.0.0.1:8080",
            "pattern_ipv4_address_port",
            {
                "ipv4-addr--679c6c82-b4be-52e2-9c7a-198689f6f77b",
                "indicator--6aadee60-d1b7-5df0-941f-02e5bb5de1db",
                "relationship--b5a0e8b5-c3ca-54e4-9f31-35c873f95955",
                "network-traffic--bc4336c7-af88-5853-a21b-f319938f9aac",
            },
            {"ipv4-addr--679c6c82-b4be-52e2-9c7a-198689f6f77b"},
        ],
        [
            "127.0.0.1/16",
            "pattern_ipv4_address_cidr",
            {
                "ipv4-addr--31e0d7f3-97af-5dce-a98a-d9f7a06ea485",
                "relationship--0e2c8cd4-b996-5b58-b7de-3e4f0b2bd99b",
                "indicator--8f27f7fc-baa0-5df0-b38f-37219d3c6739",
            },
            {"ipv4-addr--31e0d7f3-97af-5dce-a98a-d9f7a06ea485"},
        ],
        ### ipv6
        [
            "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
            "pattern_ipv6_address_only",
            {
                "relationship--ed6f1b9e-9b2e-5416-979e-9dbc33408309",
                "indicator--6bb6f199-8f7b-5deb-81c1-abb4aa94f156",
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
                "indicator--5b6d9292-0dc4-5ae8-a056-e3c2339a410a",
                "relationship--0aea6a22-e1bc-5674-9beb-6416e8242312",
            },
            {"ipv6-addr--85a85a8c-ee99-5722-946d-3c3a3270fc6f"},
        ],
        ## domain-name
        [
            "localhost",
            "pattern_host_name",
            [
                "relationship--5592b523-b49e-58d5-b9e5-ae119fb97c31",
                "domain-name--b54e23fc-08b6-5d8e-b593-bf0dfc0a49d5",
                "indicator--36ddedd6-0a85-5d03-a4d6-9dc94234155f",
            ],
            [
                "domain-name--b54e23fc-08b6-5d8e-b593-bf0dfc0a49d5",
            ],
        ],
        [
            "somewebsite.gg",
            "pattern_host_name",
            [
                "relationship--913bb795-796c-5d75-bece-72de4c28b59a",
                "indicator--c1d8c4a9-c1b8-5a49-a48d-1dd3396870eb",
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
                "indicator--ee2530b0-8d2f-5269-b554-aa68f0863757",
                "url--b427c195-2f31-55c4-a41e-ce2beb48cf01",
                "relationship--00f6d4fd-cb16-5be2-b550-a3cfab33e03c",
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
                "indicator--6dd372ad-96e9-5c53-ba71-215d2cd0e82f",
                "relationship--31c1bfa8-e432-5e81-909f-865b5dcd1a90",
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
                "indicator--093ad0da-4e79-5b91-b358-64757a563f54",
                "relationship--c2d07594-c42b-5088-9fa8-9c48598b15ed",
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
                "indicator--063b2c20-e615-5246-957b-bd181b7d2c6d",
                "file--109eb6b5-7257-568b-8a3a-146e343ac867",
                "relationship--b0c300b4-a7bb-53db-95d4-71739bf54597",
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
                "indicator--0a9132f0-b369-50f4-8787-7aeac9e1625a",
                "email-addr--c582f4d4-bea6-5dec-951e-5b5e249f8fc5",
                "relationship--9a2b82c1-9a66-55f7-b0c7-22286bf4363a",
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
                "indicator--9a227650-9421-5b58-a857-8b634d3591ee",
                "relationship--429885d5-c49b-5413-90c1-711f2a1506b6",
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
                "relationship--01591e75-f3fa-57b0-a71b-9fcdea94348c",
                "indicator--ca34f642-76ec-56e3-800c-e6addebc4f51",
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
                "indicator--0817e236-a3fb-5551-834d-4964c6f4aebd",
                "autonomous-system--3aa27478-50b5-5ab8-9da9-cdc12b657fff",
                "relationship--2205b25a-c1e0-5991-8254-bf5cc010e019",
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
                "indicator--8ac3ca0a-61d0-5430-be4e-487962837686",
                "relationship--34a6d089-990c-51c3-ad8d-4594bee07d54",
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
                "indicator--501bf7a2-83c8-5e1f-bbb7-2dc19b18c62b",
                "cryptocurrency-wallet--6e43ef66-8082-5552-80f2-95f5a44f60aa",
                "relationship--5e0101ca-7d61-53d0-88c4-c19a196ce2c1",
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
                "indicator--6fe6630f-b95c-5ea0-bbfe-159bdbed2446",
                "relationship--8edd5458-e133-5384-941e-36970ab6fa2a",
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
                "relationship--f7817e8e-6c5f-545b-b19d-c1915acbc12a",
                "indicator--19aa38b8-ef1f-5ef5-a15e-55792e6fd2de",
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
                "indicator--a1a04f9b-0314-56fd-b478-c397caa6f567",
                "relationship--bc914fa8-f5cf-5ec4-83d8-fb537ec36ad5",
                "identity--672e6dbb-e4a0-5b81-8035-c06a1961c796",  # issuer_identity
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
