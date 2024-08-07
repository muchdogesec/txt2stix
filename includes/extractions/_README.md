## Importing external data

Check what values exist in ArangoDB for generating positive tests (because test server does not always have complete records)...

### CWEs

```sql
FOR doc IN mitre_cwe_vertex_collection
  FILTER doc._stix2arango_note != "automatically imported on collection creation"
  AND doc.type == "weakness"
  LIMIT 10
  LET cweExternalId = (
    FOR ref IN doc.external_references
      FILTER ref.source_name == "cwe"
      RETURN ref.external_id
  )
  RETURN {
    "id": doc._id,
    "cweExternalId": cweExternalId
  }
```

### CVEs

```sql
FOR doc IN nvd_cve_vertex_collection
  FILTER doc._stix2arango_note != "automatically imported on collection creation"
  AND doc.type == "vulnerability"
  SORT doc.modified DESC
  LIMIT 10
  RETURN doc.name
```

### CPEs

```sql
FOR doc IN nvd_cpe_vertex_collection
  FILTER doc._stix2arango_note != "automatically imported on collection creation"
  AND doc.type == "software"
  LIMIT 10
  RETURN doc.cpe
```