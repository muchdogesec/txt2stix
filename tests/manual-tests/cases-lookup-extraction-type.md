#### lookup_mitre_atlas_id

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_mitre_atlas.txt \
	--name 'lookup_mitre_atlas_id' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions lookup_mitre_atlas_id
```

#### 2.1.1 lookup_mitre_attack_enterprise_id

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_mitre_attack_enterprise.txt \
	--name 'Test 2.1.1 lookup_mitre_attack_enterprise_id' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions lookup_mitre_attack_enterprise_id
```

* Expected count of imported object from ArangoDB = 9
	* T1174: course-of-action--00d7d21b-69d6-4797-88a2-c86f3fc97651
	* T1174: attack-pattern--b8c5c9dd-a662-479d-9428-ae745872537c
    * TA0006: x-mitre-tactic--2558fd61-8c75-4730-94c4-11926db2a263
    * TA0011: x-mitre-tactic--f72804c5-f15a-449e-a5da-2eecd181f813
    * G1006: intrusion-set--cc613a49-9bfa-4e22-98d1-15ffbb03f034
    * T1053.005: attack-pattern--005a06c6-14bf-4118-afa0-ebcd8aebb0c9
    * T1040: attack-pattern--3257eb21-f9a7-4430-8de1-d8b6e288f529
    * T1040: course-of-action--46b7ef91-4e1d-43c5-a2eb-00fa9444f6f4
    * TA0003: x-mitre-tactic--5bc1d813-693e-4823-9961-abf9af4b0e92
* Expected count of relationship objects = 9 (one for each of the above objects back to the Report object)

#### 2.1.2 lookup_mitre_attack_mobile_id

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_mitre_attack_mobile.txt \
	--name 'Test 2.1.2 lookup_mitre_attack_mobile_id' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions lookup_mitre_attack_mobile_id
```

* Expected count of imported object from ArangoDB = 9

### 3.1.3 lookup_mitre_attack_ics_id

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_mitre_attack_ics.txt \
	--name 'Test 2.1.3 lookup_mitre_attack_ics_id' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions lookup_mitre_attack_ics_id
```

### 3.1.4 lookup_mitre_capec_id

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_mitre_capec.txt \
	--name 'Test 2.1.4 lookup_mitre_capec_id' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions lookup_mitre_capec_id
```

### 3.1.5 lookup_mitre_cwe_id

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_mitre_cwe.txt \
	--name 'Test 2.1.5 lookup_mitre_cwe_id' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions lookup_mitre_cwe_id
```

### 3.1.6 lookup_attack_pattern

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/lookup_attack_pattern.txt \
	--name 'Test 2.1.6 lookup_attack_pattern' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions lookup_attack_pattern
```

### 3.1.7 lookup_campaign

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/lookup_campaign.txt \
	--name 'Test 2.1.7 lookup_campaign' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions lookup_campaign
```

### 3.1.8 lookup_course_of_action

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/lookup_course_of_action.txt \
	--name 'Test 2.1.8 lookup_course_of_action' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions lookup_course_of_action
```

### 3.1.9 lookup_identity

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/lookup_identity.txt \
	--name 'Test 2.1.9 lookup_identity' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions lookup_identity
```

### 3.1.10 lookup_infrastructure

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/lookup_infrastructure.txt \
	--name 'Test 2.1.10 lookup_infrastructure' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions lookup_infrastructure
```

### 3.1.11 lookup_intrusion_set

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/lookup_intrusion_set.txt \
	--name 'Test 2.1.11 lookup_intrusion_set' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions lookup_intrusion_set
```

### 3.1.12 lookup_malware

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/lookup_malware.txt \
	--name 'Test 2.1.12 lookup_malware' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions lookup_malware
```

### 3.1.13 lookup_threat_actor

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/lookup_threat_actor.txt \
	--name 'Test 2.1.13 lookup_threat_actor' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions lookup_threat_actor
```

### 3.1.14 lookup_tool

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/lookup_tool.txt \
	--name 'Test 2.1.14 lookup_tool' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions lookup_tool
```

### 3.1.15 lookup_country_alpha2

```shell
python3 txt2stix.py \
	--relationship_mode standard \
	--input_file tests/data/extraction_types/generic_country_alpha2.txt \
	--name 'Test 2.1.15 lookup_country_alpha2' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions lookup_country_alpha2
```