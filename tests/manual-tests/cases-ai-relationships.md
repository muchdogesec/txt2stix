### AI relationships

#### 4.0.1 testing relationship connections

```shell
python3 txt2stix.py \
	--relationship_mode ai \
	--input_file tests/data/manually_generated_reports/basic_relationship.txt \
	--name 'Test 4.0.1 Basic AI relationships' \
	--tlp_level clear \
	--confidence 100 \
	--use_extractions pattern_ipv4_address_only,pattern_domain_name_only,lookup_malware,pattern_email_address
```