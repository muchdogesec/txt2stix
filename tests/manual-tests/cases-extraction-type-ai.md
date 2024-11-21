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
	--report_id 725bc0bf-d631-4e10-9bef-74a4cf670bd8
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
	--report_id 697b24f5-d2df-4f57-aaf1-3998db5e7281
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
	--report_id 49d002da-b037-460a-9cdf-b7607bd5d99d
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
