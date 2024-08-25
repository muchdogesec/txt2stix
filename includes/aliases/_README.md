These searches are run after importing the correct data. These scripts will do this for you: https://github.com/muchdogesec/stix2arango/blob/main/utilities/README.md

Generate `mitre_cwe_name_to_id.csv`:

```sql
FOR doc IN mitre_cwe_vertex_collection
  FILTER doc._is_latest == true
  AND doc._stix2arango_note == "v4.15"
  AND IS_ARRAY(doc.external_references)
  FOR reference IN doc.external_references
    FILTER reference.source_name == "cwe"
    SORT reference.external_id ASC
    RETURN {
      name: doc.name,
      external_id: reference.external_id
    }
```

(964 results in v4.15)

Generate `mitre_capec_name_to_id.csv`:

```sql
FOR doc IN mitre_capec_vertex_collection
  FILTER doc._is_latest == true
  AND doc._stix2arango_note == "v3.9"
  AND IS_ARRAY(doc.external_references)
  FOR reference IN doc.external_references
    FILTER reference.source_name == "capec"
    RETURN {
      name: doc.name,
      external_id: reference.external_id
    }
```

(615 results in v3.9)

Generate `mitre_attack_enterprise_name_to_id.csv` (also include x_mitre_aliases):

```sql
FOR doc IN mitre_attack_enterprise_vertex_collection
  FILTER doc._is_latest == true
  AND doc._stix2arango_note == "v15.1"
  AND doc.type != "x-mitre-matrix"
  AND IS_ARRAY(doc.external_references)
  FOR reference IN doc.external_references
    FILTER reference.source_name == "mitre-attack"
    LET names = APPEND([doc.name], doc.x_mitre_aliases ? doc.x_mitre_aliases : [])
    FOR name IN UNIQUE(names)
      SORT reference.external_id ASC
      RETURN {
        name: name,
        external_id: reference.external_id
      }
```

(2254 results in v15.1)

Generate `mitre_attack_ics_name_to_id.csv` (also include x_mitre_aliases):

```sql
FOR doc IN mitre_attack_ics_vertex_collection
  FILTER doc._is_latest == true
  AND doc._stix2arango_note == "v15.1"
  AND doc.type != "x-mitre-matrix"
  AND IS_ARRAY(doc.external_references)
  FOR reference IN doc.external_references
    FILTER reference.source_name == "mitre-attack"
    LET names = APPEND([doc.name], doc.x_mitre_aliases ? doc.x_mitre_aliases : [])
    FOR name IN UNIQUE(names)
      SORT reference.external_id ASC
      RETURN {
        name: name,
        external_id: reference.external_id
      }
```

(263 results in v15.1)

Generate `mitre_attack_mobile_name_to_id.csv` (also include x_mitre_aliases):

```sql
FOR doc IN mitre_attack_mobile_vertex_collection
  FILTER doc._is_latest == true
  AND doc._stix2arango_note == "v15.1"
  AND doc.type != "x-mitre-matrix"
  AND IS_ARRAY(doc.external_references)
  FOR reference IN doc.external_references
    FILTER reference.source_name == "mitre-attack"
    LET names = APPEND([doc.name], doc.x_mitre_aliases ? doc.x_mitre_aliases : [])
    FOR name IN UNIQUE(names)
      SORT reference.external_id ASC
      RETURN {
        name: name,
        external_id: reference.external_id
      }
```

(349 results in v15.1)