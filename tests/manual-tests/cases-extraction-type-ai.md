## AI extractions with pattern versions too

### IPv4

#### ai_ipv4_address_only

OpenAI via OpenRouter

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'OpenRouter OpenAI ai_ipv4_address_only' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_ipv4_address_only \
	--ai_settings_extractions openrouter:openai/gpt-4o \
	--report_id a1d5642c-6eb6-498c-b469-6a064ae0cca1
```

OpenAI direct

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'OpenAI ai_ipv4_address_only' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_ipv4_address_only \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 38b19704-7a8c-4105-9bc5-39cceb65ed7f
```

Anthropic direct

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'Anthropic ai_ipv4_address_only' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_ipv4_address_only \
	--ai_settings_extractions anthropic:claude-3-5-sonnet-latest \
	--report_id 0ebd9ecb-44c6-42e2-b957-52ffa94a8ac2
```

Google Gemini direct

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'Google Gemini ai_ipv4_address_only' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_ipv4_address_only \
	--ai_settings_extractions gemini:models/gemini-1.5-pro-latest \
	--report_id 20464aab-3ba7-4459-829f-5d179df01179
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

### Email address

#### ai_email_address

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_email_address.txt \
	--name 'ai_email_address' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_email_address \
	--ai_settings_extractions openai:gpt-4o \
	--report_id f07f175f-b1ac-404e-b555-14c613ba9f0f
```

### MAC address

#### ai_mac_address

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_mac_address.txt \
	--name 'ai_mac_address' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_mac_address \
	--ai_settings_extractions openai:gpt-4o \
	--report_id c24a75f5-7a7d-4db8-9f9a-1b20176f9ea6
```

### Windows Registry Key

#### ai_windows_registry_key

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_windows_registry_key.txt \
	--name 'ai_windows_registry_key' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_windows_registry_key \
	--ai_settings_extractions openai:gpt-4o \
	--report_id aeb4c001-a6d0-44cf-8a8e-1ee17cf38247
```

### User agent

#### ai_user_agent

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_user_agent.txt \
	--name 'ai_user_agent' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_user_agent \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 58b2a7e5-60a5-43cf-86cf-e6d1ed0d5a48
```

### ASN

#### ai_autonomous_system_number

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_autonomous_system_number.txt \
	--name 'ai_autonomous_system_number' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_autonomous_system_number \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 1bfdedb9-b3c1-44b9-bebb-8371651350d7
```

### Cryptocurrency

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
	--report_id 61c32b8c-f901-46b9-b684-119e61b27f9a
```

#### ai_cryptocurrency_btc_wallet_transaction

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cryptocurrency_btc_wallet.txt \
	--name 'ai_cryptocurrency_btc_wallet_transaction' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_cryptocurrency_btc_wallet_transaction \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 52d2146c-798a-440f-942f-6fe039fb8995
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
	--report_id cbb2a5f9-2f30-48c0-a45d-aa51974f84a3
```

### CVE

#### ai_cve_id

_Ensure this CVE exists in your Vulmatch install and Vulmatch host set_

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cve_id.txt \
	--name 'ai_cve_id' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_cve_id \
	--ai_settings_extractions openai:gpt-4o \
	--report_id bd97c631-a992-4a83-9ee1-7c911b23cea2
```

### CPE

#### ai_cpe_uri

_Ensure this CVE exists in your Vulmatch install and Vulmatch host set_

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cpe_uri.txt \
	--name 'ai_cpe_uri' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_cpe_uri \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 71483c72-ee15-4213-aff5-61fba6f67067
```

### Bank cards

#### ai_bank_card_mastercard

_Ensure this BIN List API key set_

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_bank_card_mastercard.txt \
	--name 'ai_bank_card_mastercard' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_bank_card_mastercard \
	--ai_settings_extractions openai:gpt-4o \
	--report_id dbde8394-c094-46c5-b5cc-f0e58f3f257c
```

#### ai_bank_card_visa

_Ensure this BIN List API key set_

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_bank_card_visa.txt \
	--name 'ai_bank_card_visa' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_bank_card_visa \
	--ai_settings_extractions openai:gpt-4o \
	--report_id ad935ada-a993-4631-ab0b-57015a36880a
```

#### ai_bank_card_amex

_Ensure this BIN List API key set_

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_bank_card_amex.txt \
	--name 'ai_bank_card_amex' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_bank_card_amex \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 84f0f6f8-86f3-439b-b905-ef38ddcea262
```

#### ai_bank_card_union_pay

_Ensure this BIN List API key set_

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_bank_card_union_pay.txt \
	--name 'ai_bank_card_union_pay' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_bank_card_union_pay \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 16e8eafa-423d-4b7a-84f0-e32f224bb302
```

#### ai_bank_card_diners

_Ensure this BIN List API key set_

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_bank_card_diners.txt \
	--name 'ai_bank_card_diners' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_bank_card_diners \
	--ai_settings_extractions openai:gpt-4o \
	--report_id ddf3f977-823a-42da-9c3a-878b0d1c0d16
```

#### ai_bank_card_jcb

_Ensure this BIN List API key set_

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_bank_card_jcb.txt \
	--name 'ai_bank_card_jcb' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_bank_card_jcb \
	--ai_settings_extractions openai:gpt-4o \
	--report_id c85d2cea-0d36-418f-8a41-9e5a1fb8b6da
```

#### ai_bank_card_discover

_Ensure this BIN List API key set_

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_bank_card_discover.txt \
	--name 'ai_bank_card_discover' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_bank_card_discover \
	--ai_settings_extractions openai:gpt-4o \
	--report_id a6f61277-847c-4c4a-a251-3723aa41772b
```

### IBAN

#### ai_iban_number

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_iban_number.txt \
	--name 'ai_iban_number' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_iban_number \
	--ai_settings_extractions openai:gpt-4o \
	--report_id ecb21127-4f17-49d0-a335-cb76aa5a9440
```

### Phone number

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
	--report_id 5e177e1f-a747-41c6-878a-5983d120323a
```

## AI extractions with lookup versions too

#### ai_country

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/ai_country.txt \
	--name 'ai_country_alpha2' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_country \
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


## Generic STIX lookups

#### ai_attack_pattern

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/lookup_attack_pattern.txt \
	--name 'ai_attack_pattern' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_attack_pattern \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 9ec6d60f-76a8-4428-8923-646e176eab0b
```

#### ai_campaign

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/lookup_campaign.txt \
	--name 'ai_campaign' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_campaign \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 7ff6f6c3-8246-4a54-8055-bd53f59fb436
```

#### ai_course_of_action

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/lookup_course_of_action.txt \
	--name 'ai_course_of_action' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_course_of_action \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 29e17725-c6fc-4618-8584-841eb8402fd4
```

#### ai_identity

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/lookup_identity.txt \
	--name 'ai_identity' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_identity \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 6c66109c-565e-454a-9244-793bf59ca3bb
```

#### ai_infrastructure

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/lookup_infrastructure.txt \
	--name 'ai_infrastructure' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_infrastructure \
	--ai_settings_extractions openai:gpt-4o \
	--report_id faeb013a-e09e-4ab8-b892-362ce00ff581
```

#### ai_intrusion_set

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/lookup_intrusion_set.txt \
	--name 'ai_intrusion_set' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_intrusion_set \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 5a2ed151-96eb-482c-b0f3-0ce268b193d5
```

#### ai_malware

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/lookup_malware.txt \
	--name 'ai_malware' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_malware \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 67457a27-6f9c-4dea-9289-2cd4345de918
```

#### ai_threat_actor

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/lookup_threat_actor.txt \
	--name 'ai_threat_actor' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_threat_actor \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 5fa6d228-149b-4f7f-8f7f-f5b430c7b9b9
```

#### ai_tool

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/lookup_tool.txt \
	--name 'ai_tool' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_tool \
	--ai_settings_extractions openai:gpt-4o \
	--report_id 30dde76b-12da-42c7-afe4-97389e47fcaa
```