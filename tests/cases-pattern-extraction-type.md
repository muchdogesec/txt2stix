#### 3.1.1 pattern_ipv4_address_only

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 3.1.1 pattern_ipv4_address_only' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only
```

#### 3.1.2 pattern_ipv4_address_cidr

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_ipv4_address_cidr.txt \
	--name 'Test 3.1.2 pattern_ipv4_address_cidr' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_cidr
```

#### 3.1.3 pattern_ipv4_address_port

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_ipv4_address_port.txt \
	--name 'Test 3.1.3 pattern_ipv4_address_port' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_port
```

#### 3.1.4 pattern_ipv6_address_only

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_ipv6_address_only.txt \
	--name 'Test 3.1.4 pattern_ipv6_address_only' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv6_address_only
```

#### 3.1.5 pattern_ipv4_address_cidr

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_ipv6_address_cidr.txt \
	--name 'Test 3.1.5 pattern_ipv6_address_cidr' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv6_address_cidr
```

#### 3.1.6 pattern_ipv4_address_port

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_ipv6_address_port.txt \
	--name 'Test 3.1.6 pattern_ipv6_address_port' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv6_address_port
```

#### 3.1.7 pattern_domain_name_only

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_domain_name_only.txt \
	--name 'Test 3.1.7 pattern_domain_name_only' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_domain_name_only
```

#### 3.1.8 pattern_domain_name_subdomain

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_domain_name_subdomain.txt \
	--name 'Test 3.1.8 pattern_domain_name_subdomain' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_domain_name_subdomain
```

#### 3.1.9 pattern_url

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_url.txt \
	--name 'Test 3.1.9 pattern_url' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_url
```

#### 3.1.10 pattern_url_file

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_url_file.txt \
	--name 'Test 3.1.10 pattern_url_file' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_url_file
```

#### 3.1.11 pattern_url_path

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_url_path.txt \
	--name 'Test 3.1.11 pattern_url_path' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_url_path
```

#### 3.1.12 pattern_host_name

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_host_name.txt \
	--name 'Test 3.1.12 pattern_host_name' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_host_name
```

#### 3.1.13 pattern_host_name_subdomain

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_host_name_subdomain.txt \
	--name 'Test 3.1.13 pattern_host_name_subdomain' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_host_name_subdomain
```

#### 3.1.14 pattern_host_name_url

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_host_name_url.txt \
	--name 'Test 3.1.14 pattern_host_name_url' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_host_name_url
```

#### 3.1.15 pattern_host_name_file

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_host_name_file.txt \
	--name 'Test 3.1.15 pattern_host_name_file' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_host_name_file
```

#### 3.1.16 pattern_host_name_path

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_host_name_path.txt \
	--name 'Test 3.1.16 pattern_host_name_path' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_host_name_path
```

#### 3.1.17 pattern_file_name

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_file_name.txt \
	--name 'Test 3.1.17 pattern_file_name' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_file_name
```

#### 3.1.18 pattern_directory_windows

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_directory_windows.txt \
	--name 'Test 3.1.18 pattern_directory_windows' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_directory_windows
```

#### 3.1.19 pattern_directory_windows_with_file

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_directory_windows_with_file.txt \
	--name 'Test 3.1.19 pattern_directory_windows_with_file' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_directory_windows_with_file
```

#### 3.1.20 pattern_directory_unix

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_directory_unix.txt \
	--name 'Test 3.1.20 pattern_directory_unix' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_directory_unix
```

#### 3.1.21 pattern_directory_unix_file

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_directory_unix_file.txt \
	--name 'Test 3.1.21 pattern_directory_unix_file' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_directory_unix_file
```

#### 3.1.22 pattern_file_hash_md5

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_file_hash_md5.txt \
	--name 'Test 3.1.22 pattern_file_hash_md5' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_file_hash_md5
```

#### 3.1.23 pattern_file_hash_sha_1

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_file_hash_sha_1.txt \
	--name 'Test 3.1.23 pattern_file_hash_sha_1' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_file_hash_sha_1
```

#### 3.1.24 pattern_file_hash_sha_256

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_file_hash_sha_256.txt \
	--name 'Test 3.1.24 pattern_file_hash_sha_256' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_file_hash_sha_256
```

#### 3.1.25 pattern_file_hash_sha_512

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_file_hash_sha_512.txt \
	--name 'Test 3.1.25 pattern_file_hash_sha_512' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_file_hash_sha_512
```

#### 3.1.26 pattern_email_address

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_email_address.txt \
	--name 'Test 3.1.26 pattern_email_address' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_email_address
```

#### 3.1.27 pattern_mac_address

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_mac_address.txt \
	--name 'Test 3.1.27 pattern_mac_address' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_mac_address
```

#### 3.1.28 pattern_windows_registry_key

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_windows_registry_key.txt \
	--name 'Test 3.1.28 pattern_windows_registry_key' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_windows_registry_key
```

#### 3.1.29 pattern_user_agent

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_user_agent.txt \
	--name 'Test 3.1.29 pattern_user_agent' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_user_agent
```

#### 3.1.30 pattern_autonomous_system_number

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_autonomous_system_number.txt \
	--name 'Test 3.1.30 pattern_autonomous_system_number' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_autonomous_system_number
```

#### 3.1.31.1 pattern_cryptocurrency_btc_wallet

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_cryptocurrency_btc_wallet.txt \
	--name 'Test 3.1.31.1 pattern_cryptocurrency_btc_wallet' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_cryptocurrency_btc_wallet
```

#### 3.1.31.2 pattern_cryptocurrency_btc_wallet_transaction

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_cryptocurrency_btc_wallet.txt \
	--name 'Test 3.1.31.2 pattern_cryptocurrency_btc_wallet_transaction' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_cryptocurrency_btc_wallet_transaction
```

#### 3.1.31.3 pattern_cryptocurrency_btc_transaction

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_cryptocurrency_btc_transaction.txt \
	--name 'Test 3.1.31.3 pattern_cryptocurrency_btc_transaction' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_cryptocurrency_btc_transaction
```

#### 3.1.32 pattern_cve_id

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_cve_id.txt \
	--name 'Test 3.1.32 pattern_cve_id' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_cve_id
```

#### 3.1.33 pattern_cpe_uri

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_cpe_uri.txt \
	--name 'Test 3.1.33 pattern_cpe_uri' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_cpe_uri
```

#### 3.1.34 pattern_bank_card_mastercard

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_bank_card_mastercard.txt \
	--name 'Test 3.1.34 pattern_bank_card_mastercard' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_bank_card_mastercard
```

#### 3.1.35 pattern_bank_card_visa

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_bank_card_visa.txt \
	--name 'Test 3.1.35 pattern_bank_card_visa' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_bank_card_visa
```

#### 3.1.36 pattern_bank_card_amex

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_bank_card_amex.txt \
	--name 'Test 3.1.36 pattern_bank_card_amex' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_bank_card_amex
```

#### 3.1.37 pattern_bank_card_union_pay

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_bank_card_union_pay.txt \
	--name 'Test 3.1.37 pattern_bank_card_union_pay' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_bank_card_union_pay
```

#### 3.1.38 pattern_bank_card_diners

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_bank_card_diners.txt \
	--name 'Test 3.1.38 pattern_bank_card_diners' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_bank_card_diners
```

#### 3.1.39 pattern_bank_card_jcb

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_bank_card_jcb.txt \
	--name 'Test 3.1.39 pattern_bank_card_jcb' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_bank_card_jcb
```

#### 3.1.40 pattern_bank_card_discover

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_bank_card_discover.txt \
	--name 'Test 3.1.40 pattern_bank_card_discover' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_bank_card_discover
```

#### 3.1.41 pattern_iban_number

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_iban_number.txt \
	--name 'Test 3.1.41 pattern_iban_number' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_iban_number
```

#### 3.1.42 pattern_phone_number

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_phone_number.txt \
	--name 'Test 3.1.42 pattern_phone_number' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_phone_number
```