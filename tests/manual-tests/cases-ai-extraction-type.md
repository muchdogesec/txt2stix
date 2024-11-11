#### 1.1.1 ai_cryptocurrency_btc_wallet

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cryptocurrency_btc_wallet.txt \
	--name 'Test 1.1.1 ai_cryptocurrency_btc_wallet' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_cryptocurrency_btc_wallet \
	--ai_settings_extractions openai:gpt4o,anthropic:claude-3-5-sonnet-latest,google:models/gemini-1.5-pro-latest
```

#### 1.1.2 ai_cryptocurrency_btc_transaction

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cryptocurrency_btc_transaction.txt \
	--name 'Test 1.1.2 ai_cryptocurrency_btc_transaction' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_cryptocurrency_btc_transaction \
	--ai_settings_extractions openai:gpt4o,anthropic:claude-3-5-sonnet-latest,google:models/gemini-1.5-pro-latest
```

#### 1.1.3 ai_cryptocurrency_eth_wallet

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cryptocurrency_eth_wallet.txt \
	--name 'Test 1.1.3 ai_cryptocurrency_eth_wallet' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_cryptocurrency_eth_wallet \
	--ai_settings_extractions openai:gpt4o,anthropic:claude-3-5-sonnet-latest,google:models/gemini-1.5-pro-latest
```

#### 1.1.4 ai_cryptocurrency_eth_transaction

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cryptocurrency_eth_transaction.txt \
	--name 'Test 1.1.4 ai_cryptocurrency_eth_transaction' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_cryptocurrency_eth_transaction \
	--ai_settings_extractions openai:gpt4o,anthropic:claude-3-5-sonnet-latest,google:models/gemini-1.5-pro-latest
```

#### 1.1.5 ai_cryptocurrency_xmr_wallet

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cryptocurrency_xmr_wallet.txt \
	--name 'Test 1.1.5 ai_cryptocurrency_xmr_wallet' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_cryptocurrency_xmr_wallet \
	--ai_settings_extractions openai:gpt4o,anthropic:claude-3-5-sonnet-latest,google:models/gemini-1.5-pro-latest
```

#### 1.1.6 ai_cryptocurrency_xmr_transaction

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_cryptocurrency_xmr_transaction.txt \
	--name 'Test 1.1.6 ai_cryptocurrency_xmr_transaction' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_cryptocurrency_xmr_transaction \
	--ai_settings_extractions openai:gpt4o,anthropic:claude-3-5-sonnet-latest,google:models/gemini-1.5-pro-latest
```

#### 1.1.7 ai_phone_number

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_phone_number.txt \
	--name 'Test 1.1.7 ai_phone_number' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_phone_number \
	--ai_settings_extractions openai:gpt4o,anthropic:claude-3-5-sonnet-latest,google:models/gemini-1.5-pro-latest
```

#### 1.1.8 ai_country_alpha2

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/ai_country_alpha2.txt \
	--name 'Test 1.1.8 ai_country_alpha2' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_country_alpha2 \
	--ai_settings_extractions openai:gpt4o,anthropic:claude-3-5-sonnet-latest,google:models/gemini-1.5-pro-latest
```

#### 1.1.9 ai_mitre_attack_enterprise

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/ai_mitre_attack_enterprise.txt \
	--name 'Test 21.1.9 ai_mitre_attack_enterprise' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_mitre_attack_enterprise \
	--ai_settings_extractions openai:gpt4o,anthropic:claude-3-5-sonnet-latest,google:models/gemini-1.5-pro-latest
```

#### 1.1.10 ai_mitre_attack_mobile

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/ai_mitre_attack_mobile.txt \
	--name 'Test 1.1.10 ai_mitre_attack_mobile' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_mitre_attack_mobile \
	--ai_settings_extractions openai:gpt4o,anthropic:claude-3-5-sonnet-latest,google:models/gemini-1.5-pro-latest
```

#### 1.1.11 ai_mitre_attack_ics

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/ai_mitre_attack_ics.txt \
	--name 'Test 1.1.11 ai_mitre_attack_ics' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_mitre_attack_ics \
	--ai_settings_extractions openai:gpt4o,anthropic:claude-3-5-sonnet-latest,google:models/gemini-1.5-pro-latest
```

#### 1.1.12 ai_mitre_capec

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/ai_mitre_capec.txt \
	--name 'Test 1.1.12 ai_mitre_capec' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_mitre_capec \
	--ai_settings_extractions openai:gpt4o,anthropic:claude-3-5-sonnet-latest,google:models/gemini-1.5-pro-latest
```

#### 1.1.13 ai_mitre_cwe

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/ai_mitre_cwe.txt \
	--name 'Test 1.1.13 ai_mitre_cwe' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions ai_mitre_cwe \
	--ai_settings_extractions openai:gpt4o,anthropic:claude-3-5-sonnet-latest,google:models/gemini-1.5-pro-latest
```


#### 0.4.3 ai extractions whitelist

```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/data/extraction_types/whitelist_examples.txt \
    --name '0.4.3 Whitelist of AI with 1 known match' \
    --tlp_level clear \
    --confidence 100 \
    --use_whitelist examples_whitelist \
    --use_extractions ai_mitre_attack_enterprise \
	--ai_settings_extractions openai:gpt4o,anthropic:claude-3-5-sonnet-latest,google:models/gemini-1.5-pro-latest
```

Expect 0 extractions.

```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/data/extraction_types/whitelist_examples.txt \
    --name '0.4.3 Whitelist of AI with 1 known match' \
    --tlp_level clear \
    --confidence 100 \
    --use_extractions ai_mitre_attack_enterprise \
	--ai_settings_extractions openai:gpt4o,anthropic:claude-3-5-sonnet-latest,google:models/gemini-1.5-pro-latest
```

* course-of-action (2)
* attack-pattern (3)
* x-mitre-tactic (3)
* intrusion-set (1)
* relationship (9)


#### 0.6.3 All AI extractions

```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/data/extraction_types/all_cases.txt \
    --name '0.6.3 All test cases ai extractions' \
    --tlp_level clear \
    --confidence 100 \
    --use_extractions ai_cryptocurrency_btc_wallet,ai_cryptocurrency_btc_transaction,ai_cryptocurrency_eth_wallet,ai_cryptocurrency_eth_transaction,ai_cryptocurrency_xmr_wallet,ai_cryptocurrency_xmr_transaction,ai_phone_number,ai_country_alpha2,ai_mitre_attack_enterprise,ai_mitre_attack_mobile,ai_mitre_attack_ics,ai_mitre_capec,ai_mitre_cwe \
	--ai_settings_extractions openai:gpt4o,anthropic:claude-3-5-sonnet-latest,google:models/gemini-1.5-pro-latest
```