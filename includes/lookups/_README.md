These searches are run after importing the correct data. These scripts will do this for you: https://github.com/muchdogesec/stix2arango/blob/main/utilities/README.md

Generate `mitre_cwe_id.txt`:

```sql
FOR doc IN mitre_cwe_vertex_collection
  FILTER doc._is_latest == true
  AND doc._stix2arango_note == "v4.15"
  AND IS_ARRAY(doc.external_references)
  AND doc.x_mitre_deprecated != true
  AND doc.revoked != true
  FOR reference IN doc.external_references
    FILTER reference.source_name == "cwe"
    SORT reference.external_id ASC
    RETURN reference.external_id
```

Generate `mitre_capec_id.txt`:

```sql
FOR doc IN mitre_capec_vertex_collection
  FILTER doc._is_latest == true
  AND doc._stix2arango_note == "v3.9"
  AND doc.x_mitre_deprecated != true
  AND doc.revoked != true
  AND IS_ARRAY(doc.external_references)
  FOR reference IN doc.external_references
    FILTER reference.source_name == "capec"
    SORT reference.external_id ASC
    RETURN reference.external_id
```

Generate `mitre_attack_enterprise_id.txt`

```sql
FOR doc IN mitre_attack_enterprise_vertex_collection
  FILTER doc._is_latest == true
  AND doc._stix2arango_note == "v15.1"
  AND doc.type != "x-mitre-matrix"
  AND doc.x_mitre_deprecated != true
  AND doc.revoked != true
  AND IS_ARRAY(doc.external_references)
  FOR reference IN doc.external_references
    FILTER reference.source_name == "mitre-attack"
    SORT reference.external_id ASC
    RETURN reference.external_id
```

Generate `mitre_attack_ics_id.txt`

```sql
FOR doc IN mitre_attack_ics_vertex_collection
  FILTER doc._is_latest == true
  AND doc._stix2arango_note == "v15.1"
  AND doc.type != "x-mitre-matrix"
  AND doc.x_mitre_deprecated != true
  AND doc.revoked != true
  AND IS_ARRAY(doc.external_references)
  FOR reference IN doc.external_references
    FILTER reference.source_name == "mitre-attack"
    SORT reference.external_id ASC
    RETURN reference.external_id
```

Generate `mitre_attack_mobile_id.txt`

```sql
FOR doc IN mitre_attack_mobile_vertex_collection
  FILTER doc._is_latest == true
  AND doc._stix2arango_note == "v15.1"
  AND doc.type != "x-mitre-matrix"
  AND doc.x_mitre_deprecated != true
  AND doc.revoked != true
  AND IS_ARRAY(doc.external_references)
  FOR reference IN doc.external_references
    FILTER reference.source_name == "mitre-attack"
    SORT reference.external_id ASC
    RETURN reference.external_id
```

Generate `mitre_atlas_id.txt`

```sql
FOR doc IN mitre_atlas_vertex_collection
  FILTER doc._is_latest == true
  AND doc._stix2arango_note == "v4.5.2"
  AND doc.type != "x-mitre-matrix"
  AND doc.x_mitre_deprecated != true
  AND doc.revoked != true
  AND IS_ARRAY(doc.external_references)
  FOR reference IN doc.external_references
    FILTER reference.source_name == "mitre-atlas"
    SORT reference.external_id ASC
    RETURN reference.external_id
```
