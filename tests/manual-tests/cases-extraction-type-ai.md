### IPv4

#### ai_ipv4_address_only

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'ai_ipv4_address_only' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_ipv4_address_only \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 38b19704-7a8c-4105-9bc5-39cceb65ed7f
```

#### ai_ipv4_address_cidr

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_cidr.txt \
	--name 'ai_ipv4_address_cidr' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_ipv4_address_cidr \
	--ai_settings_extractions openai:gpt-4o \
	--report_id fc852fef-4d68-4d28-9a1b-f29940b97016
```

#### ai_ipv4_address_port

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_port.txt \
	--name 'ai_ipv4_address_port' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_ipv4_address_port \
	--ai_settings_extractions openai:gpt-4o \
	--report_id aeb1eb97-84d4-4026-8f8c-fbd784763b62
```

### IPv6

#### ai_ipv6_address_only

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv6_address_only.txt \
	--name 'ai_ipv6_address_only' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_ipv6_address_only \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 0f86dc8f-97b7-46a4-ac32-10bed0b6dfea
```

#### ai_ipv6_address_cidr

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv6_address_cidr.txt \
	--name 'ai_ipv6_address_cidr' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_ipv6_address_cidr \
	--ai_settings_extractions openai:gpt-4o \
	--report_id af9bae9a-6a40-4f87-b51c-50bd0bb4d394
```

#### ai_ipv6_address_port

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv6_address_port.txt \
	--name 'ai_ipv6_address_port' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_ipv6_address_port \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 85edd875-f3eb-4530-8604-74aa93842450
```

### Domain

#### ai_domain_name_only

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_domain_name_only.txt \
	--name 'ai_domain_name_only' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_domain_name_only \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 0804ff04-f3ef-41b0-998c-7e699a4ce916
```

#### pattern_domain_name_subdomain

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_domain_name_subdomain.txt \
	--name 'ai_domain_name_subdomain' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_domain_name_subdomain \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 19d948c9-9c33-48ef-b6df-7197119a4bd1
```

### URL

#### ai_url

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_url.txt \
	--name 'ai_url' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_url \
	--ai_settings_extractions openai:gpt-4o \
	--report_id bcd05fa3-d219-4151-9bbe-76a2eb1f77ca
```

#### ai_url_file

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_url_file.txt \
	--name 'ai_url_file' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_url_file \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 6d062894-6762-42e7-a36c-5dbad10f7b59
```

#### ai_url_path

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_url_path.txt \
	--name 'ai_url_path' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_url_path \
	--ai_settings_extractions openai:gpt-4o \
	--report_id a7e94479-b79a-4bd6-9fa8-1a4a0c43f973
```

### Hostname

#### ai_host_name

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_host_name.txt \
	--name 'ai_host_name' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_host_name \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 92b49b8b-75eb-40de-96ab-5bda4608afb2
```

#### ai_host_name_subdomain

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_host_name_subdomain.txt \
	--name 'ai_host_name_subdomain' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_host_name_subdomain \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 487bc2d3-5bb0-4413-af93-7da64b86f682
```

#### ai_host_name_url

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_host_name_url.txt \
	--name 'ai_host_name_url' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_host_name_url \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 9e113deb-71b4-4415-9266-460dbb0518d0
```

#### ai_host_name_file

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_host_name_file.txt \
	--name 'ai_host_name_file' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_host_name_file \
	--ai_settings_extractions openai:gpt-4o \
	--report_id f9b6b76e-fbde-45e8-9bfb-a739e3cc5e14
```

#### ai_host_name_path

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_host_name_path.txt \
	--name 'ai_host_name_path' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_host_name_path \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 5572ff73-9a88-4715-8a97-c12fdaea477a
```

### Directories

#### ai_directory_windows

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_directory_windows.txt \
	--name 'ai_directory_windows' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_directory_windows \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 81a7188a-4c9c-48c0-8dbb-38a591182f03
```

#### ai_directory_windows_with_file

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_directory_windows_with_file.txt \
	--name 'ai_directory_windows_with_file' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_directory_windows_with_file \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 03fe7f4f-101d-481f-ab47-5b7dd55c1e85
```

#### ai_directory_unix

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_directory_unix.txt \
	--name 'ai_directory_unix' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_directory_unix \
	--ai_settings_extractions openai:gpt-4o \
	--report_id bc82d4c1-c924-48fd-8896-82633c0bafb3
```

#### ai_directory_unix_file

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_directory_unix_file.txt \
	--name 'ai_directory_unix_file' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_directory_unix_file \
	--ai_settings_extractions openai:gpt-4o \
	--report_id b2b8e25e-44df-40b7-9a32-170d8976ee72
```

### Files

#### ai_file_name

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_file_name.txt \
	--name 'ai_file_name' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_file_name \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 86fcb9d4-f0bb-4a3b-b014-30694bd568b4
```

#### ai_file_hash_md5

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_file_hash_md5.txt \
	--name 'ai_file_hash_md5' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_file_hash_md5 \
	--ai_settings_extractions openai:gpt-4o \
	--report_id cd086fd4-3a7f-49ff-9e7d-2f024b754501
```

#### ai_file_hash_sha_1

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_file_hash_sha_1.txt \
	--name 'ai_file_hash_sha_1' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_file_hash_sha_1 \
	--ai_settings_extractions openai:gpt-4o \
	--report_id dbfda3d7-56f2-4cd1-b909-9a8f7f28667e
```

#### ai_file_hash_sha_256

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_file_hash_sha_256.txt \
	--name 'ai_file_hash_sha_256' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_file_hash_sha_256 \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 0cbfb4aa-9482-46d6-8c86-475973021378
```

#### ai_file_hash_sha_512

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_file_hash_sha_512.txt \
	--name 'ai_file_hash_sha_512' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_file_hash_sha_512 \
	--ai_settings_extractions openai:gpt-4o \
	--report_id bea70032-f6fe-4261-8aad-e11ca3a89c50
```






#### ai_cryptocurrency_btc_wallet

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cryptocurrency_btc_wallet.txt \
	--name 'ai_cryptocurrency_btc_wallet' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_cryptocurrency_btc_wallet \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 5e7330c0-aa1f-48a4-8792-9e656eed397f
```

#### ai_cryptocurrency_btc_transaction

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cryptocurrency_btc_transaction.txt \
	--name 'ai_cryptocurrency_btc_transaction' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_cryptocurrency_btc_transaction \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 61db085c-ec03-44d9-bcdf-0bd4c4f54360
```

#### ai_cryptocurrency_eth_wallet

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cryptocurrency_eth_wallet.txt \
	--name 'ai_cryptocurrency_eth_wallet' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_cryptocurrency_eth_wallet \
	--ai_settings_extractions openai:gpt-4o \
	--report_id de602a36-352e-4177-855f-5b8be50abd80
```

#### ai_cryptocurrency_eth_transaction

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cryptocurrency_eth_transaction.txt \
	--name 'ai_cryptocurrency_eth_transaction' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_cryptocurrency_eth_transaction \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 5696aaba-f3a4-4a69-bb5c-cb4f69c5a88b
```

#### ai_cryptocurrency_xmr_wallet

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cryptocurrency_xmr_wallet.txt \
	--name 'ai_cryptocurrency_xmr_wallet' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_cryptocurrency_xmr_wallet \
	--ai_settings_extractions openai:gpt-4o \
	--report_id db42c522-ad2c-4f8d-8cc2-836775e5d387
```

#### ai_cryptocurrency_xmr_transaction

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cryptocurrency_xmr_transaction.txt \
	--name 'ai_cryptocurrency_xmr_transaction' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_cryptocurrency_xmr_transaction \
	--ai_settings_extractions openai:gpt-4o \
	--report_id ce176710-435f-4490-893e-f034e8847e88
```

#### ai_phone_number

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_phone_number.txt \
	--name 'ai_phone_number' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_phone_number \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 1d78821c-b07a-4498-8174-791cf196f962
```

#### ai_country_alpha2

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/ai_country_alpha2.txt \
	--name 'ai_country_alpha2' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_country_alpha2 \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 256f89fe-ad21-4604-9d6d-b8b5335f4657
```

#### ai_mitre_attack_enterprise

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/ai_mitre_attack_enterprise.txt \
	--name 'ai_mitre_attack_enterprise' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_mitre_attack_enterprise \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 37535e3d-da26-4afd-8bae-e37f0c917c85
```

#### ai_mitre_attack_mobile

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/ai_mitre_attack_mobile.txt \
	--name 'ai_mitre_attack_mobile' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_mitre_attack_mobile \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 0751c9b2-43ab-4463-9480-1d8542f7fa6c
```

#### ai_mitre_attack_ics

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/ai_mitre_attack_ics.txt \
	--name 'ai_mitre_attack_ics' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_mitre_attack_ics \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 949a0740-69c7-4c78-bedc-c78917360b57
```

#### ai_mitre_capec

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/ai_mitre_capec.txt \
	--name 'ai_mitre_capec' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_mitre_capec \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 7a1aed89-5aef-4e14-8453-019d8375e08d
```

#### ai_mitre_cwe

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/ai_mitre_cwe.txt \
	--name 'ai_mitre_cwe' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_mitre_cwe \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 6ba5c857-86be-4016-9490-7b83b2d18105
```
