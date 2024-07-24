### Generic tests

#### 0.1.1 Test TLP levels

Clear

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.1 Clear' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only
```
Green

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.1 Green' \
	--tlp_level green \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only
```

Amber

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.1 Amber' \
	--tlp_level amber \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only
```

Amber+Strict

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.1 Amber+Strict' \
	--tlp_level amber_strict \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only
```

Red

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.1 Red' \
	--tlp_level red \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only
```

Bad TLP value -- should return error

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_ipv4_address_only.txt \
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
	--input_file tests/inputs/extraction_types/generic_ipv4_address_only.txt \
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
	--input_file tests/inputs/extraction_types/generic_ipv4_address_only.txt \
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
	--input_file tests/inputs/extraction_types/generic_ipv4_address_only.txt \
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
	--input_file tests/inputs/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.3 Confidence score not passed' \
	--tlp_level clear \
	--use_extractions ai_ipv4_address_only
```

---

Bad confidence value (out of range 0-100) -- should return error

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_ipv4_address_only.txt \
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
	--input_file tests/inputs/manually_generated_reports/char_length_too_long.txt \
	--name 'Test 0.1.4 File too many chars' \
	--tlp_level amber \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only
```

#### 0.1.5 Labels

Adding good labels, expect to see 2 labels in report:

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_ipv4_address_only.txt \
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
	--input_file tests/inputs/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.5 Bad labels' \
	--tlp_level amber \
	--labels label_1,labels2 \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only
```

#### 0.1.6 Created time

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/inputs/extraction_types/generic_ipv4_address_only.txt \
	--name 'Test 0.1.5 Created time' \
	--tlp_level green \
	--created 2020-01-01T00:00:00.000Z \
	--use_extractions pattern_ipv4_address_only
```

### AI relationship mode tests

#### 0.2.1 A descriptive example with all extraction types in txt file enabled (no external objects)

```shell
python3 txt2stix.py \
	--relationship_mode ai \
	--input_file tests/inputs/manually_generated_reports/descriptive_for_ai_relationships_1.txt \
	--name 'Test 0.2.1 Lots of descriptive relationships' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only,pattern_url,lookup_country_alpha2,pattern_autonomous_system_number,lookup_malware,pattern_file_hash_sha_256,lookup_mitre_attack_enterprise_id
```

### Aliasing

#### 0.3.1

```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/inputs/manually_generated_reports/test_aliases.txt \
    --name '0.3.1 Test All Default Aliases in Standard relationships mode' \
    --tlp_level clear \
    --confidence 100 \
    --use_aliases country_iso3166_alpha3_to_alpha2,country_name_to_iso2,mitre_cwe_name_to_id,mitre_capec_name_to_id,mitre_attack_enterprise_name_to_id,mitre_attack_ics_name_to_id,mitre_attack_mobile_name_to_id \
    --use_extractions lookup_country_alpha2,lookup_mitre_cwe_id,lookup_mitre_capec_id,lookup_mitre_attack_enterprise_id,lookup_mitre_attack_ics_id,lookup_mitre_attack_mobile_id
```

The original values -> alias values -> extraction type:

1. GBR -> GB -> `location` + `relationship` + `indicator`
2. United Kingdom -> GB -> `location` + `indicator` + `relationship` (not created as same as entry 1)
3. Hidden Users Mitigation (ATT&CK Enterprise only) -> T1147 -> `attack-pattern` + `relationship` + `course-of-action` + `relationship`
4. Limit Access to Resource Over Network (ATT&CK Enterprise and ICS) -> M1035 (Enterprise) / M0935 (ICS) -> `course-of-action` + `relationship` (Enterprise) + `course-of-action` + `relationship` (ICS)
5. Brute Force -> CAPEC-112 (CAPEC) / T1110 (ATT&CK Enterprise) -> `attack-pattern` + `relationship` (CAPEC) + `course-of-action` + `relationship` (Enterprise)
7. Static Member Data Element outside of a Singleton Class Element -> CWE-1042 -> `weakness` + `relationship`

* location (1)
* course-of-action (4)
* attack-pattern (2)
* weakness (1)
* indicator (1)
* relationship (8)

---

Same input / extractions, but testing AI relationships...

```shell
python3 txt2stix.py \
    --relationship_mode ai \
    --input_file tests/inputs/manually_generated_reports/test_aliases.txt \
    --name '0.3.1 Test All Default Aliases in Standard relationships mode' \
    --tlp_level clear \
    --confidence 100 \
    --use_aliases country_iso3166_alpha3_to_alpha2,country_name_to_iso2,mitre_cwe_name_to_id,mitre_capec_name_to_id,mitre_attack_enterprise_name_to_id,mitre_attack_ics_name_to_id,mitre_attack_mobile_name_to_id \
    --use_extractions lookup_country_alpha2,lookup_mitre_cwe_id,lookup_mitre_capec_id,lookup_mitre_attack_enterprise_id,lookup_mitre_attack_ics_id,lookup_mitre_attack_mobile_id
```

### Whitelisting

#### 0.4.1 pattern extractions whitelist

Contains `google.com` which matches whitelist. Also contains `signalcorps.com` which does not match whitelist.

```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/inputs/extraction_types/whitelist_alexa_top_1000_domains.txt \
    --name '0.4.1 Whitelist with 1 known match, 1 unknown' \
    --tlp_level clear \
    --confidence 100 \
    --use_whitelist alexa_top_1000_domains \
    --use_extractions pattern_domain_name_only
```

Expect

* indicator (1)
* domain-name (1)
* relationship (1)

Here is the same input, this time without whitelist:

```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/inputs/extraction_types/whitelist_alexa_top_1000_domains.txt \
    --name '0.4.1 Whitelist with 1 known match, 1 unknown' \
    --tlp_level clear \
    --confidence 100 \
    --use_extractions pattern_domain_name_only
```

Expect

* indicator (2)
* domain-name (2)
* relationship (2)

#### 0.4.2 lookup extractions whitelist

```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/inputs/extraction_types/whitelist_examples.txt \
    --name '0.4.2 Whitelist of Lookup with 1 known match' \
    --tlp_level clear \
    --confidence 100 \
    --use_extractions lookup_mitre_attack_enterprise_id
```

Expect

* course-of-action (1)
* attack-pattern (1)
* relationship (2)

```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/inputs/extraction_types/whitelist_examples.txt \
    --name '0.4.2 Whitelist of Lookup with 1 known match' \
    --tlp_level clear \
    --confidence 100 \
    --use_whitelist examples_whitelist \
    --use_extractions lookup_mitre_attack_enterprise_id
```

Expect 0 extractions

#### 0.4.3 ai extractions whitelist

```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/inputs/extraction_types/whitelist_examples.txt \
    --name '0.4.3 Whitelist of AI with 1 known match' \
    --tlp_level clear \
    --confidence 100 \
    --use_whitelist examples_whitelist \
    --use_extractions ai_mitre_attack_enterprise
```

Expect 0 extractions.

```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/inputs/extraction_types/whitelist_examples.txt \
    --name '0.4.3 Whitelist of AI with 1 known match' \
    --tlp_level clear \
    --confidence 100 \
    --use_extractions ai_mitre_attack_enterprise
```

* course-of-action (2)
* attack-pattern (3)
* x-mitre-tactic (3)
* intrusion-set (1)
* relationship (9)

#### 0.4.4 Where whitelist value appears in string

```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/inputs/extraction_types/generic_url_path.txt \
    --name '0.4.4 Where whitelist value appears in string no whitelist' \
    --tlp_level clear \
    --confidence 100 \
    --use_extractions pattern_url_path
```

https://fortinet.com/blog should extract


```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/inputs/extraction_types/generic_url_path.txt \
    --name '0.4.4 Where whitelist value appears in string with whitelist' \
    --tlp_level clear \
    --confidence 100 \
    --use_whitelist security_vendor_domains \
    --use_extractions pattern_url_path
```

https://fortinet.com/blog will still extract because only `fortinet.com` is in the `security_vendor_domains` whitelist and the match needs to be exact.

### Extractions escapes

#### 0.5.1

https://github.com/signalscorps/txt2stix/blob/beta-1/design/mvp/extraction-types.md#a-note-on-extraction-logic-for-pattern-lookup-extraction-types-and-aliasing

```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/inputs/manually_generated_reports/test_extraction_escapes.txt \
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
    --input_file tests/inputs/extraction_types/all_cases.txt \
    --name '0.6.1 All test cases pattern extractions' \
    --tlp_level clear \
    --confidence 100 \
    --use_extractions pattern_ipv4_address_only,pattern_ipv4_address_cidr,pattern_ipv4_address_port,pattern_ipv6_address_only,pattern_ipv6_address_cidr,pattern_ipv6_address_port,pattern_domain_name_only,pattern_domain_name_subdomain,pattern_url,pattern_url_file,pattern_url_path,pattern_host_name,pattern_host_name_subdomain,pattern_host_name_url,pattern_host_name_file,pattern_host_name_path,pattern_file_name,pattern_directory_windows,pattern_directory_windows_with_file,pattern_directory_unix,pattern_directory_unix_file,pattern_file_hash_md5,pattern_file_hash_sha_1,pattern_file_hash_sha_256,pattern_file_hash_sha_512,pattern_email_address,pattern_mac_address,pattern_windows_registry_key,pattern_user_agent,pattern_autonomous_system_number,pattern_cryptocurrency_btc_wallet,pattern_cve_id,pattern_cpe_uri,pattern_bank_card_mastercard,pattern_bank_card_visa,pattern_bank_card_amex,pattern_bank_card_union_pay,pattern_bank_card_diners,pattern_bank_card_jcb,pattern_bank_card_discover,pattern_iban_number,pattern_phone_number
```

#### 0.6.2 All Lookup extractions

```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/inputs/extraction_types/all_cases.txt \
    --name '0.6.2 All test cases lookup extractions' \
    --tlp_level clear \
    --confidence 100 \
    --use_extractions lookup_mitre_attack_enterprise_id,lookup_mitre_attack_mobile_id,lookup_mitre_attack_ics_id,lookup_mitre_capec_id,lookup_mitre_cwe_id,lookup_country_alpha2,lookup_attack_pattern,lookup_campaign,lookup_course_of_action,lookup_identity,lookup_infrastructure,lookup_intrusion_set,lookup_malware,lookup_threat_actor,lookup_tool
```

#### 0.6.3 All AI extractions

```shell
python3 txt2stix.py \
    --relationship_mode standard \
    --input_file tests/inputs/extraction_types/all_cases.txt \
    --name '0.6.3 All test cases ai extractions' \
    --tlp_level clear \
    --confidence 100 \
    --use_extractions ai_cryptocurrency_btc_wallet,ai_cryptocurrency_btc_transaction,ai_cryptocurrency_eth_wallet,ai_cryptocurrency_eth_transaction,ai_cryptocurrency_xmr_wallet,ai_cryptocurrency_xmr_transaction,ai_phone_number,ai_country_alpha2,ai_mitre_attack_enterprise,ai_mitre_attack_mobile,ai_mitre_attack_ics,ai_mitre_capec,ai_mitre_cwe
```