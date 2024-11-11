### AI relationships doc 1

#### 4.0.1 testing relationship connections OpenAI

```shell
python3 txt2stix.py \
	--relationship_mode ai \
	--ai_settings_relationships openai:gpt4o \
	--input_file tests/data/manually_generated_reports/basic_relationship.txt \
	--name 'Test 4.0.1 Basic AI relationships openai' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only,pattern_domain_name_only,lookup_malware,pattern_email_address
```

#### 4.0.2 testing relationship connections Anthropic

```shell
python3 txt2stix.py \
	--relationship_mode ai \
	--ai_settings_relationships anthropic:claude-3-5-sonnet-latest \
	--input_file tests/data/manually_generated_reports/basic_relationship.txt \
	--name 'Test 4.0.2 Basic AI relationships anthropic' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only,pattern_domain_name_only,lookup_malware,pattern_email_address
```

#### 4.0.3 testing relationship connections Google

```shell
python3 txt2stix.py \
	--relationship_mode ai \
	--ai_settings_relationships google:gemini-1.5-pro-latest \
	--input_file tests/data/manually_generated_reports/basic_relationship.txt \
	--name 'Test 4.0.3 Basic AI relationships Google' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only,pattern_domain_name_only,lookup_malware,pattern_email_address
```

### AI relationships doc 2

#### 4.1.1 testing more relationship connections OpenAI

```shell
python3 txt2stix.py \
	--relationship_mode ai \
	--ai_settings_relationships openai:gpt4o \
	--input_file tests/data/manually_generated_reports/descriptive_for_ai_relationships_1.txt \
	--name 'Test 4.1.1 Basic AI relationships openai' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only,pattern_url,lookup_country_alpha2,pattern_autonomous_system_number,lookup_malware,pattern_file_hash_sha_256,lookup_mitre_attack_enterprise_id
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
	--use_extractions pattern_ipv4_address_only,pattern_url,lookup_country_alpha2,pattern_autonomous_system_number,lookup_malware,pattern_file_hash_sha_256,lookup_mitre_attack_enterprise_id
```

#### 4.1.3 testing more relationship connections Google

```shell
python3 txt2stix.py \
	--relationship_mode ai \
	--ai_settings_relationships google:gemini-1.5-pro-latest \
	--input_file tests/data/manually_generated_reports/descriptive_for_ai_relationships_1.txt \
	--name 'Test 4.1.3 Basic AI relationships google' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only,pattern_url,lookup_country_alpha2,pattern_autonomous_system_number,lookup_malware,pattern_file_hash_sha_256,lookup_mitre_attack_enterprise_id
```