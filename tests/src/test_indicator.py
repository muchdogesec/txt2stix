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

from txt2stix.bundler import txt2stixBundler
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
                "indicator--a07184da-7d33-5b13-b877-66baa3584a7b",
                "ipv4-addr--679c6c82-b4be-52e2-9c7a-198689f6f77b",
                "relationship--453f41f2-9b4b-5bee-ac6b-d87a9bed49d2",
            },
            {"ipv4-addr--679c6c82-b4be-52e2-9c7a-198689f6f77b"},
            id="ipv4 address_only",
        ),
        pytest.param(
            "127.0.0.1:8080",
            "pattern_ipv4_address_port",
            {
                "indicator--f06eba73-0dc3-5b4c-a4b2-b8cdcbbb1092",
                "ipv4-addr--679c6c82-b4be-52e2-9c7a-198689f6f77b",
                "relationship--913dfcb5-171e-5590-8f8b-bd352eb8300f",
                "network-traffic--bc4336c7-af88-5853-a21b-f319938f9aac",
            },
            {"ipv4-addr--679c6c82-b4be-52e2-9c7a-198689f6f77b"},
            id="ipv4 address_port",
        ),
        pytest.param(
            "127.0.0.1/16",
            "pattern_ipv4_address_cidr",
            {
                "indicator--f47753fc-5f96-5e2c-b798-38c34f0664dd",
                "ipv4-addr--31e0d7f3-97af-5dce-a98a-d9f7a06ea485",
                "relationship--a0eaec93-7b0e-5e4d-93f8-5be37003e6f6",
            },
            {"ipv4-addr--31e0d7f3-97af-5dce-a98a-d9f7a06ea485"},
            id="ipv4 address_cidr",
        ),
        pytest.param(
            "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
            "pattern_ipv6_address_only",
            {
                "indicator--d06f2f5b-168a-5b73-8cca-237b44e94ed1",
                "ipv6-addr--85a85a8c-ee99-5722-946d-3c3a3270fc6f",
                "relationship--d26c2e27-e958-5167-b9f2-371a16198666",
            },
            {"ipv6-addr--85a85a8c-ee99-5722-946d-3c3a3270fc6f"},
            id="ipv6 address_only",
        ),
        pytest.param(
            "[2001:0db8:85a3:0000:0000:8a2e:0370:7334]:8080",
            "pattern_ipv6_address_port",
            {
                "indicator--d3cffad2-d934-5f1f-829c-342fd8956b74",
                "ipv6-addr--85a85a8c-ee99-5722-946d-3c3a3270fc6f",
                "relationship--20d02821-de20-5768-b381-be3de55a292d",
                "network-traffic--d7f1aefc-12ba-53d6-a2c8-c54d7b956e39",
            },
            {"ipv6-addr--85a85a8c-ee99-5722-946d-3c3a3270fc6f"},
            id="ipv6 address_port",
        ),
        ## domain-name
        pytest.param(
            "localhost",
            "pattern_host_name",
            {
                "indicator--03057a6b-18bf-5ab9-95e4-844198c060bb",
                "domain-name--b54e23fc-08b6-5d8e-b593-bf0dfc0a49d5",
                "relationship--85afb679-5915-54c2-9d08-2375e95b76bf",
            },
            [
                "domain-name--b54e23fc-08b6-5d8e-b593-bf0dfc0a49d5",
            ],
            id="domain-name host_name",
        ),
        pytest.param(
            "somewebsite.gg",
            "pattern_host_name",
            {
                "indicator--b71ed37a-8095-5590-aa39-9056b6ecc722",
                "domain-name--6b8b0382-6675-5d04-8442-5a1e2d9e903f",
                "relationship--8e1d2945-d2d5-5868-9dac-1a8bf6a65639",
            },
            [
                "domain-name--6b8b0382-6675-5d04-8442-5a1e2d9e903f",
            ],
            id="domain-name 2",
        ),
        ## url
        pytest.param(
            "http://localhost:123/die",
            "pattern_url",
            {
                "indicator--d10d08c7-71a8-53ec-aacd-7b06b51fe38b",
                "url--b427c195-2f31-55c4-a41e-ce2beb48cf01",
                "relationship--c71a6941-e1e1-5863-a99b-aa296459ebac",
            },
            [
                "url--b427c195-2f31-55c4-a41e-ce2beb48cf01",
            ],
            id="url",
        ),
        ## file
        pytest.param(
            "file.jpg",
            "pattern_file_name",
            {
                "indicator--b161ae03-688d-5cf3-ab7e-ad7ccc07cc9a",
                "file--a525dace-961b-5749-b9c3-3e2feba0034c",
                "relationship--92627fe0-92dd-5d6b-917f-a57bd5af9af6",
            },
            [
                "file--a525dace-961b-5749-b9c3-3e2feba0034c",
            ],
            id="file",
        ),
        ## directory-file
        pytest.param(
            "/path/to/dir/die.exe",
            "pattern_directory_unix_file",
            {
                "indicator--8dfdfdcc-0136-5528-90ca-75b32960a63a",
                "directory--1377fe61-b48b-5250-985b-db5ff7f97200",
                "file--68fbb6e6-6111-54ef-b3dc-850a8e91d3d8",
                "relationship--85af7eb4-14ba-5bce-b207-5eac43bc844f",
            },
            [
                "file--68fbb6e6-6111-54ef-b3dc-850a8e91d3d8",
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
                "relationship--04024c50-4a29-5cbc-8f29-50d2795bc1fb",
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
                "relationship--56bb515e-9cc1-5462-ae0b-ab8f97594af7",
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
                "mac-addr--757b1725-9903-54f5-a855-1240691d7659",
                "relationship--0af3497f-6c7d-584e-b60c-14e678835d65",
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
                "indicator--5b176858-f869-52d3-b04b-326fd434766f",
                "windows-registry-key--3be35eea-0b2d-5316-8f7d-46daf6b5029e",
                "relationship--b89375ea-e3ed-519c-9961-3d8fa0cc0739",
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
                "relationship--af53acfb-3325-59bd-bcf8-de633e16531a",
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
                "indicator--0eb12807-33c5-5d5a-b465-164ef424bd9a",
                "user-agent--b71ac3f9-2e75-5f59-ada4-71e8a2514ec3",
                "relationship--1dccc75d-d7e5-50a5-8939-4658d9ff7681",
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
                "cryptocurrency-wallet--201124c3-52c3-5f89-8a48-94deb554c6c6",
                "relationship--14e27f6d-d938-5199-b89d-d7cecb22539a",
                "indicator--b8374546-ecf1-51e5-b4f3-f0e021af8f4d",
            },
            {
                "cryptocurrency-wallet--201124c3-52c3-5f89-8a48-94deb554c6c6",
            },
            id="cryptocurrency-wallet",
        ),
        ## bank-account
        [
            "DE29100500001061045672",
            "pattern_iban_number",
            {
                "indicator--816dfb00-4107-5dd0-be00-4607400f4df3",
                "bank-account--4e351d05-b4f5-5d7e-b51e-66e92021ba5a",
                "relationship--97947636-acc1-5a2f-971f-cfeee373e75e",
            },
            {
                "bank-account--4e351d05-b4f5-5d7e-b51e-66e92021ba5a",
            },
        ],
        ## phone-number
        [
            "+442083661177",
            "pattern_phone_number",
            {
                "indicator--c955785e-d762-5e11-8e0d-27e255361669",
                "phone-number--f3ea8fdf-ef0f-5711-a105-7fcb1c289dc6",
                "relationship--706c4917-4481-592d-aadc-28e0b28ee4e1",
            },
            {
                "phone-number--f3ea8fdf-ef0f-5711-a105-7fcb1c289dc6",
            },
        ],
        ## bank-card, with issuer-name
        pytest.param(
            "5555555555554444",
            "pattern_bank_card_mastercard",
            {
                "identity--7d46a822-1e99-5c73-ac5e-dec6400977ab",
                "relationship--1de7fbdc-3796-5d42-9efa-5bcdf2bb01cd",
                "relationship--03a31907-32ae-5f83-80a7-37dbe0ed61c2",
                "indicator--3dfe8be8-cb89-5872-a162-329be05ddfb7",
                "location--24ff45f2-9cd3-554c-a53c-2ed70bb17cb8",
                "payment-card--45b2fea7-587b-5ccf-a9b2-e0fa748d6423",
            },
            {
                "payment-card--45b2fea7-587b-5ccf-a9b2-e0fa748d6423",
            },
            id="bank-card, with issuer-name",
        ),
        ## bank-card, no issuer-name
        pytest.param(
            "376654224631002",
            "pattern_bank_card_amex",
            {
                "indicator--5a5a66de-62f3-5262-8c29-2f314c6ce738",
                "relationship--b5d9a3fc-9fb0-5c45-acbe-acf88d70b17b",
                "identity--643246fc-9204-5b4b-976d-2e605b355c24",
                "payment-card--683af74c-c39f-5ca1-8366-7781f8ac7685",
            },
            {
                "payment-card--683af74c-c39f-5ca1-8366-7781f8ac7685",
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
    print({obj["id"] for obj in objects})
    assert {obj["id"] for obj in objects} == set(expected_objects)
    assert {id for id in relationships} == set(expected_rels)


@pytest.mark.parametrize(
    "extractor_name",
    {
        v.test_cases: k
        for k, v in all_extractors.items()
        if v.test_cases != "ai_country"
    }.values(),
)
def test_build_observables_with_extractor_cases__positive(extractor_name, subtests):
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


@pytest.mark.parametrize(
    "extractor_name",
    {
        v.test_cases: k
        for k, v in all_extractors.items()
        if (
            not v.test_cases.startswith("generic_bank")
            and not v.test_cases.startswith("lookup_")
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
        )
    }.values(),
)
def test_build_observables_with_extractor_cases__negative(extractor_name, subtests):
    extractor = all_extractors[extractor_name]
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
