### IPv4

#### pattern_ipv4_address_only

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'pattern_ipv4_address_only' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only \
	--report_id a41ef56e-bcf4-4d1c-9f07-11019c5986ab
```

#### pattern_ipv4_address_cidr

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_cidr.txt \
	--name 'pattern_ipv4_address_cidr' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_cidr \
	--report_id 8ead91c4-a1b7-46b9-bb4a-58e164f55f41
```

#### pattern_ipv4_address_port

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_port.txt \
	--name 'pattern_ipv4_address_port' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_port \
	--report_id 4e4dd170-095e-452a-b4d3-88feebcb595b
```

### IPv6

#### pattern_ipv6_address_only

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv6_address_only.txt \
	--name 'pattern_ipv6_address_only' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv6_address_only \
	--report_id 6aca0879-e88f-4914-9d92-075a7c6c8c46
```

#### pattern_ipv6_address_cidr

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv6_address_cidr.txt \
	--name 'pattern_ipv6_address_cidr' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv6_address_cidr \
	--report_id d6c538f6-7c89-43ae-8e0b-4751600d766c
```

#### pattern_ipv6_address_port

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv6_address_port.txt \
	--name 'pattern_ipv6_address_port' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv6_address_port \
	--report_id b8392b27-8715-496e-acc2-f64220a4db3d
```

### Domain

#### pattern_domain_name_only

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_domain_name_only.txt \
	--name 'pattern_domain_name_only' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_domain_name_only \
	--report_id 2b6deed4-a5ce-4ee2-bca2-0333dede5df2
```

#### pattern_domain_name_subdomain

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_domain_name_subdomain.txt \
	--name 'pattern_domain_name_subdomain' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_domain_name_subdomain \
	--report_id 8f4ec53f-41f7-419c-af3a-82ed54abbbb1
```

### URL

#### pattern_url

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_url.txt \
	--name 'pattern_url' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_url \
	--report_id 725bc0bf-d631-4e10-9bef-74a4cf670bd8
```

#### pattern_url_file

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_url_file.txt \
	--name 'pattern_url_file' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_url_file \
	--report_id 697b24f5-d2df-4f57-aaf1-3998db5e7281
```

#### pattern_url_path

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_url_path.txt \
	--name 'pattern_url_path' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_url_path \
	--report_id 49d002da-b037-460a-9cdf-b7607bd5d99d
```

### Hostname

#### pattern_host_name

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_host_name.txt \
	--name 'pattern_host_name' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_host_name \
	--report_id 0323a5f9-c1af-407c-b823-a47e9f8d0f99
```

#### pattern_host_name_subdomain

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_host_name_subdomain.txt \
	--name 'pattern_host_name_subdomain' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_host_name_subdomain \
	--report_id bfc8d87c-305a-4364-a0e6-aaef4ac37c0c
```

#### pattern_host_name_url

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_host_name_url.txt \
	--name 'pattern_host_name_url' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_host_name_url \
	--report_id f7957152-0281-466e-9ac6-b813dc387a8b
```

#### pattern_host_name_file

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_host_name_file.txt \
	--name 'pattern_host_name_file' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_host_name_file \
	--report_id 8e84c874-6036-4283-8e4d-053237de073a
```

#### pattern_host_name_path

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_host_name_path.txt \
	--name 'pattern_host_name_path' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_host_name_path \
	--report_id cce19848-d2c9-4af1-a2ab-0eddf545b476
```

### Directories

#### pattern_directory_windows

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_directory_windows.txt \
	--name 'pattern_directory_windows' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_directory_windows \
	--report_id 27208f08-119e-4c0a-a706-b8f009d1bf10
```

#### pattern_directory_windows_with_file

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_directory_windows_with_file.txt \
	--name 'pattern_directory_windows_with_file' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_directory_windows_with_file \
	--report_id 15341a31-345d-4aa1-a550-feaa3cb4e80a
```

#### pattern_directory_unix

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_directory_unix.txt \
	--name 'pattern_directory_unix' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_directory_unix \
	--report_id 6084a58f-468f-4acb-8933-2e61fb549a18
```

#### pattern_directory_unix_file

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_directory_unix_file.txt \
	--name 'pattern_directory_unix_file' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_directory_unix_file \
	--report_id ed473f19-2651-408a-8400-06c1fea66dcc
```

### Files

#### pattern_file_name

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_file_name.txt \
	--name 'pattern_file_name' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_file_name \
	--report_id 6fb55a1b-1317-419d-9e7b-67e174c08eb2
```

#### pattern_file_hash_md5

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_file_hash_md5.txt \
	--name 'pattern_file_hash_md5' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_file_hash_md5 \
	--report_id 0b4534b0-68ba-4a3a-bfe0-6fea5a9aedc9
```

#### pattern_file_hash_sha_1

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_file_hash_sha_1.txt \
	--name 'pattern_file_hash_sha_1' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_file_hash_sha_1 \
	--report_id aa904c54-0c8c-4ed2-ad9b-ff314b89d200
```

#### pattern_file_hash_sha_256

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_file_hash_sha_256.txt \
	--name 'pattern_file_hash_sha_256' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_file_hash_sha_256 \
	--report_id b5528feb-2e56-4091-9818-fd04fcde02ee
```

#### pattern_file_hash_sha_512

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_file_hash_sha_512.txt \
	--name 'pattern_file_hash_sha_512' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_file_hash_sha_512 \
	--report_id d0268862-3e4b-4085-b802-217d61b08f86
```

### Email address

#### pattern_email_address

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_email_address.txt \
	--name 'pattern_email_address' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_email_address \
	--report_id 5e94cb03-4677-4de1-93d6-0f417c5906a6
```

### MAC address

#### pattern_mac_address

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_mac_address.txt \
	--name 'pattern_mac_address' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_mac_address \
	--report_id 292d54ca-6952-45c4-b10e-3b5aae27eb55
```

### Windows Registry Key

#### pattern_windows_registry_key

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_windows_registry_key.txt \
	--name 'pattern_windows_registry_key' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_windows_registry_key \
	--report_id d49dd6f2-82fe-419d-9b37-e1ba441b54eb
```

### User agent

#### pattern_user_agent

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_user_agent.txt \
	--name 'pattern_user_agent' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_user_agent \
	--report_id ed1c8308-dc64-4bc5-a9d3-2996845eaf92
```

### ASN

#### pattern_autonomous_system_number

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_autonomous_system_number.txt \
	--name 'pattern_autonomous_system_number' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_autonomous_system_number \
	--report_id 0667a32d-296c-40b7-9c0d-8dc5f55f78af
```

### Cryptocurrency

#### pattern_cryptocurrency_btc_wallet

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cryptocurrency_btc_wallet.txt \
	--name 'pattern_cryptocurrency_btc_wallet' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_cryptocurrency_btc_wallet \
	--report_id 99d651b2-5165-4c2e-81f6-ad7bd3670167
```

#### pattern_cryptocurrency_btc_wallet_transaction

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cryptocurrency_btc_wallet.txt \
	--name 'pattern_cryptocurrency_btc_wallet_transaction' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_cryptocurrency_btc_wallet_transaction \
	--report_id 2e1ae2e2-664e-420a-a35b-8720801e8500
```

#### pattern_cryptocurrency_btc_transaction

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cryptocurrency_btc_transaction.txt \
	--name 'pattern_cryptocurrency_btc_transaction' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_cryptocurrency_btc_transaction \
	--report_id 7eecca51-0496-45f4-be2d-204a0d54ebb3
```

### CVE

#### pattern_cve_id

_Ensure this CVE exists in your Vulmatch install and Vulmatch host set_

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cve_id.txt \
	--name 'pattern_cve_id' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_cve_id \
	--report_id 478cebce-1c14-4ed5-b2fb-ee6dde03d88b
```

### CPE

#### pattern_cpe_uri

_Ensure this CVE exists in your Vulmatch install and Vulmatch host set_

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cpe_uri.txt \
	--name 'pattern_cpe_uri' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_cpe_uri \
	--report_id f035f034-adc0-4689-88e0-542aa87ef2c4
```

### Bank cards

#### pattern_bank_card_mastercard

_Ensure this BIN List API key set_

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_bank_card_mastercard.txt \
	--name 'pattern_bank_card_mastercard' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_bank_card_mastercard \
	--report_id 12efa579-7628-458d-ac62-90d699438af8
```

#### pattern_bank_card_visa

_Ensure this BIN List API key set_

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_bank_card_visa.txt \
	--name 'pattern_bank_card_visa' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_bank_card_visa \
	--report_id 5d4f148d-ef81-4b60-a35e-a49d69098e7a
```

#### pattern_bank_card_amex

_Ensure this BIN List API key set_

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_bank_card_amex.txt \
	--name 'pattern_bank_card_amex' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_bank_card_amex \
	--report_id a04c5a06-d79b-46be-823c-c275ee805a09
```

#### pattern_bank_card_union_pay

_Ensure this BIN List API key set_

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_bank_card_union_pay.txt \
	--name 'pattern_bank_card_union_pay' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_bank_card_union_pay \
	--report_id 5108b602-3a35-478b-8be4-6a896c56b229
```

#### pattern_bank_card_diners

_Ensure this BIN List API key set_

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_bank_card_diners.txt \
	--name 'pattern_bank_card_diners' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_bank_card_diners \
	--report_id e3d71ee4-c176-4c8b-9334-cb79a1cd910f
```

#### pattern_bank_card_jcb

_Ensure this BIN List API key set_

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_bank_card_jcb.txt \
	--name 'pattern_bank_card_jcb' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_bank_card_jcb \
	--report_id f6180309-e5fa-419b-91b5-77f9bafc2319
```

#### pattern_bank_card_discover

_Ensure this BIN List API key set_

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_bank_card_discover.txt \
	--name 'pattern_bank_card_discover' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_bank_card_discover \
	--report_id 27999387-d8be-4673-9ca7-7805d2254d1c
```

### IBAN

#### pattern_iban_number

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_iban_number.txt \
	--name 'pattern_iban_number' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_iban_number \
	--report_id 191174f6-84e2-432d-a147-83adf5f19ecd
```

### Phone number

#### pattern_phone_number

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_phone_number.txt \
	--name 'pattern_phone_number' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_phone_number \
	--report_id cc242c57-2440-4abc-a382-5683aea9d588
```