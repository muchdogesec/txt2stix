Put any notes about aliases in here.

Import data to arango as follows;

https://github.com/muchdogesec/stix2arango/blob/main/backfill_scripts/backfill.md

Generate mitre_cwe_name_to_id:

```sql
FOR doc IN mitre_cwe_vertex_collection
  FILTER IS_ARRAY(doc.external_references)
  FOR reference IN doc.external_references
    FILTER reference.source_name == "cwe"
    RETURN {
      name: doc.name,
      external_id: reference.external_id
    }
```

Generate mitre_capec_name_to_id:

```sql
FOR doc IN mitre_capec_vertex_collection
  FILTER IS_ARRAY(doc.external_references)
  FOR reference IN doc.external_references
    FILTER reference.source_name == "capec"
    RETURN {
      name: doc.name,
      external_id: reference.external_id
    }
```

Generate mitre_attack_enterprise_name_to_id:

```sql
FOR doc IN mitre_attack_enterprise_vertex_collection
  FILTER IS_ARRAY(doc.external_references)
  FOR reference IN doc.external_references
    FILTER reference.source_name == "mitre-attack"
    LIMIT @offset, @count
    RETURN {
      name: doc.name,
      external_id: reference.external_id
    }
```

Returns more than 1000 results, so need to set offset

Generate mitre_attack_ics_name_to_id:

```sql
FOR doc IN mitre_attack_ics_vertex_collection
  FILTER IS_ARRAY(doc.external_references)
  FOR reference IN doc.external_references
    FILTER reference.source_name == "mitre-attack"
    RETURN {
      name: doc.name,
      external_id: reference.external_id
    }
```

Generate mitre_attack_mobile_name_to_id:

```sql
FOR doc IN mitre_attack_mobile_vertex_collection
  FILTER IS_ARRAY(doc.external_references)
  FOR reference IN doc.external_references
    FILTER reference.source_name == "mitre-attack"
    RETURN {
      name: doc.name,
      external_id: reference.external_id
    }
```