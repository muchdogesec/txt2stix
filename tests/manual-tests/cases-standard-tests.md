#### 0.1.1 Test TLP levels

Clear

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.1 Clear' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only
```
Green

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.1 Green' \
	--tlp_level green \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only
```

Amber

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.1 Amber' \
	--tlp_level amber \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only
```

Amber+Strict

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.1 Amber+Strict' \
	--tlp_level amber_strict \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only
```

Red

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.1 Red' \
	--tlp_level red \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only
```

Bad TLP value -- should return error

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.1 Bad TLP value' \
	--tlp_level bad \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only
```

#### 0.1.2 Passing a custom identity

Following should use default identity `identity--9c259ff7-f413-5001-9911-70b4352af93f`

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.2 Custom Identity' \
	--tlp_level amber_strict \
	--confidence 90 \
	--use_extractions pattern_ipv4_address_only
```

Check only that identity (`identity--9c259ff7-f413-5001-9911-70b4352af93f`) is in bundle and the all objects have it as `created_by_ref`

---

Following should PASS as Identity is valid:

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.2 Custom Identity' \
	--tlp_level amber_strict \
	--confidence 90 \
	--use_identity '{"type":"identity","spec_version":"2.1","id":"identity--d2916708-57b9-5636-8689-62f049e9f727","created_by_ref":"identity--aae8eb2d-ea6c-56d6-a606-cc9f755e2dd3","created":"2020-01-01T00:00:00.000Z","modified":"2020-01-01T00:00:00.000Z","name":"signalscorps-demo","description":"https://github.com/signalscorps/","identity_class":"organization","sectors":["technology"],"contact_information":"https://www.signalscorps.com/contact/","object_marking_refs":["marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9","marking-definition--3f588e96-e413-57b5-b735-f0ec6c3a8771"]}' \
	--use_extractions pattern_ipv4_address_only
```

Check only that identity (`identity--d2916708-57b9-5636-8689-62f049e9f727`) is in bundle and the all objects have it as `created_by_ref`

---

Following should FAIL as Identity is bad:

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.2 Custom Identity' \
	--tlp_level amber_strict \
	--confidence 90 \
	--use_identity '{"id":"identity--d2916708-57b9-5636-8689-62f049e9f727","created_by_ref":"identity--aae8eb2d-ea6c-56d6-a606-cc9f755e2dd3","created":"2020-01-01T00:00:00.000Z","modified":"2020-01-01T00:00:00.000Z","name":"signalscorps-demo","description":"https://github.com/signalscorps/","identity_class":"organization","sectors":["technology"],"contact_information":"https://www.signalscorps.com/contact/","object_marking_refs":["marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9","marking-definition--3f588e96-e413-57b5-b735-f0ec6c3a8771"]}' \
	--use_extractions pattern_ipv4_address_only
```

#### 0.1.3 Confidence score

Confidence score not passed, is valid (no `confidence` property in report)

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.3 Confidence score not passed' \
	--tlp_level clear \
	--use_extractions pattern_ipv4_address_only
```

---

Bad confidence value (out of range 0-100) -- should return error

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.1 Bad Confidence value' \
	--tlp_level clear \
	--confidence 1000 \
	--use_extractions pattern_ipv4_address_only
```

#### 0.1.4 Passing a file longer than default `INPUT_CHARACHTER_LIMIT`

Set `INPUT_CHARACTER_LIMIT= 50000` in `.env` file and this test should fail:

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/manually_generated_reports/char_length_too_long.txt \
	--name 'Test 0.1.4 File too many chars' \
	--tlp_level amber \
	--confidence 100 \
	--use_extractions ai_ipv4_address_only \
	--ai_settings_extractions openai
```

#### 0.1.5 Labels

Adding good labels, expect to see 2 labels in report:

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.5 Good labels' \
	--tlp_level amber \
	--labels label1,labels2 \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only
```

One bad label as not `a-z`, `0-9`, should error

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.5 Bad labels' \
	--tlp_level amber \
	--labels label_1,labels2 \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only
```

#### 0.1.6 Created time

when created is passed, modified and created should be the same.

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.5 Created time' \
	--tlp_level green \
	--created 2020-01-01T00:00:00.000Z \
	--use_extractions pattern_ipv4_address_only
```

### Extractions escapes

#### 0.5.1


```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/data/manually_generated_reports/test_extraction_escapes.txt \
    --name '0.5.1 Test extraction escapes in pattern mode' \
    --tlp_level clear \
    --confidence 100 \
    --use_extractions pattern_ipv4_address_only
```

Here 7 IPs will be extracted. But this may vary depending on how AI is feeling!

### Large volume of extractions

#### 0.6.1 All Pattern extractions

```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/data/extraction_types/all_cases.txt \
    --name '0.6.1 All test cases pattern extractions' \
    --tlp_level clear \
    --confidence 100 \
    --use_extractions pattern_ipv4_address_only,pattern_ipv4_address_cidr,pattern_ipv4_address_port,pattern_ipv6_address_only,pattern_ipv6_address_cidr,pattern_ipv6_address_port,pattern_domain_name_only,pattern_domain_name_subdomain,pattern_url,pattern_url_file,pattern_url_path,pattern_host_name,pattern_host_name_subdomain,pattern_host_name_url,pattern_host_name_file,pattern_host_name_path,pattern_file_name,pattern_directory_windows,pattern_directory_windows_with_file,pattern_directory_unix,pattern_directory_unix_file,pattern_file_hash_md5,pattern_file_hash_sha_1,pattern_file_hash_sha_256,pattern_file_hash_sha_512,pattern_email_address,pattern_mac_address,pattern_windows_registry_key,pattern_user_agent,pattern_autonomous_system_number,pattern_cryptocurrency_btc_wallet,pattern_cve_id,pattern_cpe_uri,pattern_bank_card_mastercard,pattern_bank_card_visa,pattern_bank_card_amex,pattern_bank_card_union_pay,pattern_bank_card_diners,pattern_bank_card_jcb,pattern_bank_card_discover,pattern_iban_number,pattern_phone_number
```

#### 0.6.2 All Lookup extractions

```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/data/extraction_types/all_cases.txt \
    --name '0.6.2 All test cases lookup extractions' \
    --tlp_level clear \
    --confidence 100 \
    --use_extractions lookup_mitre_attack_enterprise_id,lookup_mitre_attack_mobile_id,lookup_mitre_attack_ics_id,lookup_mitre_capec_id,lookup_mitre_cwe_id,lookup_country_alpha2,lookup_attack_pattern,lookup_campaign,lookup_course_of_action,lookup_identity,lookup_infrastructure,lookup_intrusion_set,lookup_malware,lookup_threat_actor,lookup_tool
```

### 0.7 passing report id

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.7 Using report id 62611965-930e-43db-8b95-30a1e119d7e2' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only \
	--report_id 62611965-930e-43db-8b95-30a1e119d7e2
```

### 0.8 test custom external_refernces

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.7 Using report id 62611965-930e-43db-8b95-30a1e119d7e2' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only \
	--external_refs key=value source=id
```

### ignore image refs

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/manually_generated_reports/embedded_img_ignore.txt \
	--name 'ignore image refs true' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_domain_name_only,pattern_domain_name_subdomain,pattern_url,pattern_file_name \
	--ignore_image_refs true \
	--report_id 649da017-4090-48b2-97da-b24d37418ee6
```

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/manually_generated_reports/embedded_img_ignore.txt \
	--name 'ignore image refs false' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_domain_name_only,pattern_domain_name_subdomain,pattern_url,pattern_file_name \
	--ignore_image_refs false \
	--report_id 669f7663-18e0-4381-90c8-6622c06b16ec
```

### ignore link refs

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/manually_generated_reports/embedded_link_ignore.txt \
	--name 'ignore link refs true' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_domain_name_only,pattern_domain_name_subdomain,pattern_url,pattern_file_name \
	--ignore_link_refs true \
	--report_id 8854f8c9-f231-4f4b-8145-4db95b1d13cf
```

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/manually_generated_reports/embedded_link_ignore.txt \
	--name 'ignore link refs false' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_domain_name_only,pattern_domain_name_subdomain,pattern_url,pattern_file_name \
	--ignore_link_refs false \
	--report_id 8cf2590e-f7b8-40c6-99cd-4aad9fbdc8bd
```

### Report UUIDs

Ip1

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/manually_generated_reports/ip1.txt \
	--name 'ip1' \
	--use_extractions pattern_ipv4_address_only \
	--report_id c36664ff-be15-455e-9dea-8d1161f67feb
```

Ip2 same IP as Ip1, but slightly different MD5

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/manually_generated_reports/ip2.txt \
	--name 'ip2' \
	--use_extractions pattern_ipv4_address_only \
	--report_id e0a7ea6f-e61a-4fbf-b61e-00bab0d20e50
```

IP2 but with identity

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/manually_generated_reports/ip2.txt \
	--name 'ip2 with ID' \
	--use_identity '{"type":"identity","spec_version":"2.1","id":"identity--d2916708-57b9-5636-8689-62f049e9f727","created_by_ref":"identity--aae8eb2d-ea6c-56d6-a606-cc9f755e2dd3","created":"2020-01-01T00:00:00.000Z","modified":"2020-01-01T00:00:00.000Z","name":"signalscorps-demo","description":"https://github.com/signalscorps/","identity_class":"organization","sectors":["technology"],"contact_information":"https://www.signalscorps.com/contact/","object_marking_refs":["marking-definition--613f2e26-407d-48c7-9eca-b8e91df99dc9","marking-definition--3f588e96-e413-57b5-b735-f0ec6c3a8771"]}' \
	--use_extractions pattern_ipv4_address_only \
	--report_id b7bca3c9-5577-4794-96c4-4e4715b5fde7
```

### extraction boundary tests

Should create `pattern_url_file` extraction as boundary observed

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/manually_generated_reports/test_extraction_boundary.txt \
	--name 'extraction boundary tests 1' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions 'pattern_*' \
	--report_id f6d8800b-9708-4c74-aa1b-7a59d3c79d79
```

Should create all extractions;

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/manually_generated_reports/test_extraction_boundary.txt \
	--name 'extraction boundary tests 1' \
	--tlp_level clear \
	--confidence 100 \
	--ignore_extraction_boundary true \
	--use_extractions 'pattern_*' \
	--report_id 0f5b1afd-c468-49a2-9896-6910b7f124dd
```

### disarm demo

```shell
python3 txt2stix.py \
	--relationship_mode ai \
	--ai_settings_relationships openai:gpt-4o \
	--input_file tests/data/manually_generated_reports/disarm_demo.txt \
	--name 'DISARM demo' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions lookup_disarm_name \
	--report_id 8cb2dbf0-136f-4ecb-995c-095496e22abc
```

### ai check content

```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/data/extraction_types/all_cases.txt \
    --name 'Test AI Content check' \
    --tlp_level clear \
    --confidence 100 \
    --use_extractions 'pattern_*' \
    --ai_content_check_provider openai:gpt-4o \
    --report_id 4fa18f2d-278b-4fd4-8470-62a8807d35ad
```

The following should not be passed to AI (not security content)

```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/data/manually_generated_reports/not_security_content.txt \
    --name 'Test AI Content check failure' \
    --tlp_level clear \
    --confidence 100 \
	--use_extractions ai_ipv4_address_only \
	--ai_settings_extractions openai:gpt-4o \
    --ai_content_check_provider openai:gpt-4o \
    --ai_extract_if_no_incidence false \
    --report_id ed6039d6-699c-44f0-9bf0-957d4d0ff99f
```

 Will pass but still process, as `ai_content_check_provider` is omitted

```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/data/extraction_types/all_cases.txt \
    --name 'Test AI Content check failure' \
    --tlp_level clear \
    --confidence 100 \
	--use_extractions ai_ipv4_address_only \
	--ai_settings_extractions openai:gpt-4o \
    --tlp_level clear \
    --confidence 100 \
	--use_extractions ai_ipv4_address_only \
	--ai_settings_extractions openai:gpt-4o \
	--ai_extract_if_no_incidence false \
    --report_id 2880d1c1-0211-45b6-8565-befe596ff81f
```

### attack flow demo

no indicators

```shell
python3 txt2stix.py \
    --relationship_mode ai \
    --ai_settings_relationships openai:gpt-4o \
    --input_file tests/data/manually_generated_reports/attack_flow_demo.txt \
    --name 'Test MITRE ATT&CK Flow demo' \
    --tlp_level clear \
    --confidence 100 \
    --use_extractions 'ai_mitre_attack_enterprise' \
    --ai_settings_extractions openai:gpt-4o \
    --ai_create_attack_flow \
    --report_id c0fef67c-720b-4184-a62e-ea465b4d89b5
```

with indicators

```shell
python3 txt2stix.py \
    --relationship_mode ai \
    --ai_settings_relationships openai:gpt-4o \
    --input_file tests/data/manually_generated_reports/attack_flow_demo.txt \
    --name 'Test MITRE ATT&CK Flow demo with iocs' \
    --tlp_level clear \
    --confidence 100 \
    --use_extractions ai_mitre_attack_enterprise,'pattern_*' \
    --ai_settings_extractions openai:gpt-4o \
    --ai_create_attack_flow \
    --report_id 3b160a8d-12dd-4e7c-aee8-5af6e371b425
```

with two domains

no indicators

```shell
python3 txt2stix.py \
    --relationship_mode ai \
    --ai_settings_relationships openai:gpt-5 \
    --input_file tests/data/manually_generated_reports/attack_flow_demo.txt \
    --name 'Test MITRE ATT&CK Flow demo' \
    --tlp_level clear \
    --confidence 100 \
    --use_extractions 'ai_mitre_attack_*' \
    --ai_settings_extractions openai:gpt-5 \
    --ai_create_attack_flow \
    --report_id ccc8c844-6a89-4762-b4e7-77c918fa4b8f
```

### attack navigator demo

```shell
python3 txt2stix.py \
    --relationship_mode ai \
    --ai_settings_relationships openai:gpt-4o \
    --input_file tests/data/manually_generated_reports/attack_navigator_demo.txt \
    --name 'Test MITRE ATT&CK Navigator' \
    --tlp_level clear \
    --confidence 100 \
    --use_extractions 'ai_mitre_attack_*' \
    --ai_settings_extractions openai:gpt-4o \
    --ai_create_attack_navigator_layer \
    --ai_content_check_provider openai:gpt-4o \
    --report_id b599f044-f22c-4e38-a2ed-3ef43442ccd2
```

`ai_content_check_provider` checked to ensure summary is used as description

### attack navigator and attack flow

used to check prompts only sent once

```shell
python3 txt2stix.py \
    --relationship_mode ai \
    --ai_settings_relationships openai:gpt-4o \
    --input_file tests/data/manually_generated_reports/attack_navigator_demo.txt \
    --name 'Test MITRE ATT&CK Flow and Navigator' \
    --tlp_level clear \
    --confidence 100 \
    --use_extractions 'ai_mitre_attack_enterprise' \
    --ai_settings_extractions openai:gpt-4o \
    --ai_create_attack_flow \
    --ai_create_attack_navigator_layer \
    --report_id c0d48262-1d9f-42d2-aa29-f0cba1bfa2e0
```

### test AI extraction position

same extraction twice in doc

```shell
python3 txt2stix.py \
    --relationship_mode ai \
    --ai_settings_relationships openai:gpt-4o \
    --input_file tests/data/manually_generated_reports/ai_index_position.txt \
    --name 'Extraction index' \
    --tlp_level clear \
    --confidence 100 \
    --use_extractions 'ai_ipv4_address_only' \
    --ai_settings_extractions openai:gpt-4o \
    --report_id 2b3326b4-dfcf-4391-b550-e91652f9ffcd
```