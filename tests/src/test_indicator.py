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
        ## ipv4
        pytest.param(
            "127.0.0.1",
            "pattern_ipv4_address_only",
            {
                "ipv4-addr--679c6c82-b4be-52e2-9c7a-198689f6f77b",
                "indicator--a07184da-7d33-5b13-b877-66baa3584a7b",
                "relationship--ebee86fd-def4-5ba4-9f7d-01e8d858d14c",
            },
            {"ipv4-addr--679c6c82-b4be-52e2-9c7a-198689f6f77b"},
            id="ipv4 address_only",
        ),
        pytest.param(
            "127.0.0.1:8080",
            "pattern_ipv4_address_port",
            {
                "ipv4-addr--679c6c82-b4be-52e2-9c7a-198689f6f77b",
                "indicator--f06eba73-0dc3-5b4c-a4b2-b8cdcbbb1092",
                "relationship--a69f0136-208b-5cd5-926b-b3672835d6e2",
                "network-traffic--bc4336c7-af88-5853-a21b-f319938f9aac",
            },
            {"ipv4-addr--679c6c82-b4be-52e2-9c7a-198689f6f77b"},
            id="ipv4 address_port",
        ),
        pytest.param(
            "127.0.0.1/16",
            "pattern_ipv4_address_cidr",
            {
                "ipv4-addr--31e0d7f3-97af-5dce-a98a-d9f7a06ea485",
                "relationship--47dbbaa3-8d12-5f83-95b4-7bb726918609",
                "indicator--f47753fc-5f96-5e2c-b798-38c34f0664dd",
            },
            {"ipv4-addr--31e0d7f3-97af-5dce-a98a-d9f7a06ea485"},
            id="ipv4 address_cidr",
        ),
        pytest.param(
            "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
            "pattern_ipv6_address_only",
            {
                "relationship--29b5f001-5134-5cd2-aeb0-ef8bd55d844f",
                "indicator--d06f2f5b-168a-5b73-8cca-237b44e94ed1",
                "ipv6-addr--85a85a8c-ee99-5722-946d-3c3a3270fc6f",
            },
            {"ipv6-addr--85a85a8c-ee99-5722-946d-3c3a3270fc6f"},
            id="ipv6 address_only",
        ),
        pytest.param(
            "[2001:0db8:85a3:0000:0000:8a2e:0370:7334]:8080",
            "pattern_ipv6_address_port",
            {
                "ipv6-addr--85a85a8c-ee99-5722-946d-3c3a3270fc6f",
                "network-traffic--d7f1aefc-12ba-53d6-a2c8-c54d7b956e39",
                "indicator--d3cffad2-d934-5f1f-829c-342fd8956b74",
                "relationship--fa0d2483-2945-51c8-80eb-7476e1332dfb",
            },
            {"ipv6-addr--85a85a8c-ee99-5722-946d-3c3a3270fc6f"},
            id="ipv6 address_port",
        ),
        ## domain-name
        pytest.param(
            "localhost",
            "pattern_host_name",
            [
                "relationship--b0eef578-e3eb-510b-9aa7-2c15b28e01b5",
                "domain-name--b54e23fc-08b6-5d8e-b593-bf0dfc0a49d5",
                "indicator--03057a6b-18bf-5ab9-95e4-844198c060bb",
            ],
            [
                "domain-name--b54e23fc-08b6-5d8e-b593-bf0dfc0a49d5",
            ],
            id="domain-name host_name",
        ),
        pytest.param(
            "somewebsite.gg",
            "pattern_host_name",
            [
                "relationship--753bccf7-ba02-5cf2-a57f-18784376e475",
                "indicator--b71ed37a-8095-5590-aa39-9056b6ecc722",
                "domain-name--6b8b0382-6675-5d04-8442-5a1e2d9e903f",
            ],
            [
                "domain-name--6b8b0382-6675-5d04-8442-5a1e2d9e903f",
            ],
            id="domain-name 2",
        ),
        ## url
        pytest.param(
            "http://localhost:123/die",
            "pattern_url",
            [
                "indicator--d10d08c7-71a8-53ec-aacd-7b06b51fe38b",
                "url--b427c195-2f31-55c4-a41e-ce2beb48cf01",
                "relationship--10151382-60ec-5d82-ae23-6ce97b0a24de",
            ],
            [
                "url--b427c195-2f31-55c4-a41e-ce2beb48cf01",
            ],
            id="url",
        ),
        ## file
        pytest.param(
            "file.jpg",
            "pattern_file_name",
            [
                "indicator--b161ae03-688d-5cf3-ab7e-ad7ccc07cc9a",
                "relationship--058f1b3c-76c2-535f-9d76-9af66a18d52b",
                "file--a525dace-961b-5749-b9c3-3e2feba0034c",
            ],
            [
                "file--a525dace-961b-5749-b9c3-3e2feba0034c",
            ],
            id="file",
        ),
        ## directory-file
        pytest.param(
            "/path/to/dir/die.exe",
            "pattern_directory_unix_file",
            [
                "relationship--53204f97-f4c3-59ca-9158-f0c973efd8d9",
                "file--7dbeff1a-48b6-5060-a637-04fa55f93c9a",
                "directory--1377fe61-b48b-5250-985b-db5ff7f97200",
                "indicator--8dfdfdcc-0136-5528-90ca-75b32960a63a",
                "relationship--836ea44f-01b5-5289-92da-78d187fb446e",
            ],
            [
                "directory--1377fe61-b48b-5250-985b-db5ff7f97200",
            ],
            id="directory-file",
        ),
        ## file-hash
        pytest.param(
            "86F7E437FAA5A7FCE15D1DDCB9EAEAEA377667B8",
            "pattern_file_hash_sha_1",
            {
                "indicator--0f78e264-e09c-529a-a0eb-d9361fe6d834",
                "file--109eb6b5-7257-568b-8a3a-146e343ac867",
                "relationship--b00a63f9-0fbc-53ee-a834-6928c2f0ea47",
            },
            {
                "file--109eb6b5-7257-568b-8a3a-146e343ac867",
            },
            id="file-hash",
        ),
        ## email-addr
        pytest.param(
            "goo@gmail.com",
            "pattern_email_address",
            {
                "indicator--e2d8050a-70d4-5771-9eff-3e74b4f7cfbe",
                "email-addr--c582f4d4-bea6-5dec-951e-5b5e249f8fc5",
                "relationship--90f13460-c196-58cc-881b-d7722402cc03",
            },
            {
                "email-addr--c582f4d4-bea6-5dec-951e-5b5e249f8fc5",
            },
            id="email-addr",
        ),
        ## mac-addr
        pytest.param(
            "d2:fb:49:24:37:18",
            "pattern_mac_address",
            {
                "indicator--46587123-5b01-53f0-aa5f-3fdd863b8286",
                "relationship--f89ad49c-c2fc-531e-b443-dc4bed8a37f6",
                "mac-addr--757b1725-9903-54f5-a855-1240691d7659",
            },
            {
                "mac-addr--757b1725-9903-54f5-a855-1240691d7659",
            },
            id="mac-addr",
        ),
        ## windows-registry-key
        pytest.param(
            r"HKLM\Short\\Name",
            "pattern_windows_registry_key",
            {
                "relationship--bae5abb6-a073-5995-ac00-0b16bc840af2",
                "indicator--5b176858-f869-52d3-b04b-326fd434766f",
                "windows-registry-key--3be35eea-0b2d-5316-8f7d-46daf6b5029e",
            },
            {
                "windows-registry-key--3be35eea-0b2d-5316-8f7d-46daf6b5029e",
            },
            id="windows-registry-key",
        ),
        ## autonomous-system
        pytest.param(
            "ASN15139",
            "pattern_autonomous_system_number",
            {
                "indicator--de09fba1-dc47-5cf5-a461-53aba2228fe6",
                "autonomous-system--3aa27478-50b5-5ab8-9da9-cdc12b657fff",
                "relationship--62692c31-7fd3-5f5b-8906-bbda95261600",
            },
            {
                "autonomous-system--3aa27478-50b5-5ab8-9da9-cdc12b657fff",
            },
            id="autonomous-system",
        ),
        ## user-agent
        pytest.param(
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.6) Gecko/20040113",
            "pattern_user_agent",
            {
                "user-agent--b71ac3f9-2e75-5f59-ada4-71e8a2514ec3",
                "indicator--0eb12807-33c5-5d5a-b465-164ef424bd9a",
                "relationship--9961afd0-fc4b-5a9f-96fa-129434422337",
            },
            {
                "user-agent--b71ac3f9-2e75-5f59-ada4-71e8a2514ec3",
            },
            id="user-agent",
        ),
        ## cryptocurrency-wallet
        pytest.param(
            "3Cwgr2g7vsi1bXDUkpEnVoRLA9w4FZfC69",
            "pattern_cryptocurrency_btc_wallet",
            {
                "indicator--b8374546-ecf1-51e5-b4f3-f0e021af8f4d",
                "cryptocurrency-wallet--6e43ef66-8082-5552-80f2-95f5a44f60aa",
                "relationship--547c0e2c-01b7-5bea-8611-9c5ced2c347c",
            },
            {
                "cryptocurrency-wallet--6e43ef66-8082-5552-80f2-95f5a44f60aa",
            },
            id="cryptocurrency-wallet",
        ),
        ## bank-account
        [
            "DE29100500001061045672",
            "pattern_iban_number",
            {
                "bank-account--4c1507ea-fdde-556b-87c9-f8ef702a0d8a",
                "indicator--816dfb00-4107-5dd0-be00-4607400f4df3",
                "relationship--c932782d-f9fa-5b84-9804-17403a91e074",
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
                "relationship--ef574e75-7d5a-5406-a7b6-720266cfcae9",
                "indicator--c955785e-d762-5e11-8e0d-27e255361669",
            },
            {
                "phone-number--9c0e11b8-10e5-5384-96ae-b3fe7799eb5e",
            },
        ],
        ## bank-card, with issuer-name
        pytest.param(
            "5555555555554444",
            "pattern_bank_card_mastercard",
            {
                "bank-card--fb992b79-5bd1-5aa9-bc7e-a785b28f4338",
                "indicator--3dfe8be8-cb89-5872-a162-329be05ddfb7",
                "identity--868572ea-db58-592a-a426-2cd243d748b6",
                "relationship--ad2fa28f-0fc0-5a23-acc4-4326849b620b",  # issuer_identity, with name
            },
            {
                "bank-card--fb992b79-5bd1-5aa9-bc7e-a785b28f4338",
            },
            id="bank-card, with issuer-name",
        ),
        ## bank-card, no issuer-name
        pytest.param(
            "376654224631002",
            "pattern_bank_card_amex",
            {
                "bank-card--e19f1547-2b5f-5f3d-82dc-817c7ba15405",
                "indicator--5a5a66de-62f3-5262-8c29-2f314c6ce738",
                "relationship--2bf39b70-e24d-5275-80bb-7de015e93f23",
                "identity--643246fc-9204-5b4b-976d-2e605b355c24",  # issuer_identity, no name
            },
            {
                "bank-card--e19f1547-2b5f-5f3d-82dc-817c7ba15405",
            },
            id="bank-card, no issuer-name",
        ),
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
