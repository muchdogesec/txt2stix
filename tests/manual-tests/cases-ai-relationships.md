### AI relationships doc 1

#### 4.0.1 testing relationship connections OpenAI

```shell
python3 txt2stix.py \
	--relationship_mode ai \
	--ai_settings_relationships openai:gpt-4o \
	--input_file tests/data/manually_generated_reports/basic_relationship.txt \
	--name 'Basic AI relationships openai' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only,pattern_domain_name_only,lookup_malware,pattern_email_address \
	--report_id 4da51a55-9664-4851-abd3-34d6ced5fedd
```

#### 4.0.2 testing relationship connections Anthropic

```shell
python3 txt2stix.py \
	--relationship_mode ai \
	--ai_settings_relationships anthropic:claude-3-5-sonnet-latest \
	--input_file tests/data/manually_generated_reports/basic_relationship.txt \
	--name 'Basic AI relationships anthropic' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only,pattern_domain_name_only,lookup_malware,pattern_email_address \
	--report_id 3067b8c0-3be2-4331-a891-b3b458604bb3
```

#### 4.0.3 testing relationship connections Google

```shell
python3 txt2stix.py \
	--relationship_mode ai \
	--ai_settings_relationships gemini:models/gemini-1.5-pro-latest \
	--input_file tests/data/manually_generated_reports/basic_relationship.txt \
	--name 'Basic AI relationships Google' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only,pattern_domain_name_only,lookup_malware,pattern_email_address \
	--report_id 989e9d82-7868-4cad-b0d8-b4b328781a91
```

#### 4.0.4 testing relationship connections OpenRouter Open AI

```shell
python3 txt2stix.py \
	--relationship_mode ai \
	--ai_settings_relationships openrouter:openai/gpt-4o \
	--input_file tests/data/manually_generated_reports/basic_relationship.txt \
	--name 'Basic AI OpenRouter OpenAI' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only,pattern_domain_name_only,lookup_malware,pattern_email_address \
	--report_id 247644ef-996f-474d-a963-3f7b2150577e
```

### AI relationships doc 2

#### 4.1.1 testing more relationship connections OpenAI

```shell
python3 txt2stix.py \
	--relationship_mode ai \
	--ai_settings_relationships openai:gpt-4o \
	--input_file tests/data/manually_generated_reports/descriptive_for_ai_relationships_1.txt \
	--name 'Test 4.1.1 Basic AI relationships openai' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only,pattern_url,lookup_country_alpha2,pattern_autonomous_system_number,lookup_malware,pattern_file_hash_sha_256,lookup_mitre_attack_enterprise_id \
	--report_id affe70cc-5935-44ac-a9b2-9065203b9f66
```

#### 4.1.2 testing more relationship connections Anthropic

```shell
python3 txt2stix.py \
	--relationship_mode ai \
	--ai_settings_relationships anthropic:claude-3-5-sonnet-latest \
	--input_file tests/data/manually_generated_reports/descriptive_for_ai_relationships_1.txt \
	--name 'Test 4.1.2 Basic AI relationships anthropic' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only,pattern_url,lookup_country_alpha2,pattern_autonomous_system_number,lookup_malware,pattern_file_hash_sha_256,lookup_mitre_attack_enterprise_id \
	--report_id 0cbc9608-0441-4090-ab5f-ec6e7c6b352b
```

#### 4.1.3 testing more relationship connections Google

```shell
python3 txt2stix.py \
	--relationship_mode ai \
	--ai_settings_relationships gemini:models/gemini-1.5-pro-latest \
	--input_file tests/data/manually_generated_reports/descriptive_for_ai_relationships_1.txt \
	--name 'Test 4.1.3 Basic AI relationships google' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only,pattern_url,lookup_country_alpha2,pattern_autonomous_system_number,lookup_malware,pattern_file_hash_sha_256,lookup_mitre_attack_enterprise_id \
	--report_id 753942a4-e12e-460b-a0cb-a56e8bf0ea51
```

#### 4.1.4 testing more relationship connections Google

```shell
python3 txt2stix.py \
	--relationship_mode ai \
	--ai_settings_relationships openrouter:openai/gpt-4o \
	--input_file tests/data/manually_generated_reports/descriptive_for_ai_relationships_1.txt \
	--name 'Test 4.1.3 Basic AI relationships OpenRouter OpenAI' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only,pattern_url,lookup_country_alpha2,pattern_autonomous_system_number,lookup_malware,pattern_file_hash_sha_256,lookup_mitre_attack_enterprise_id \
	--report_id 67e6556c-5a71-43c2-87f5-19b08a576e29
```