import os
from arango import ArangoClient

# Connect to ArangoDB
client = ArangoClient()
db = client.db('ctibutler_database', username='root', password='')

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define queries and output files
queries = {
    "mitre_cwe_id_v4_15.txt": """
        FOR doc IN mitre_cwe_vertex_collection
          FILTER doc._stix2arango_note == "version=4_15"
          AND IS_ARRAY(doc.external_references)
          AND doc.x_mitre_deprecated != true
          AND doc.revoked != true
          FOR reference IN doc.external_references
            FILTER reference.source_name == "cwe"
            SORT reference.external_id ASC
            RETURN reference.external_id
    """,
    "mitre_cwe_name_v4_15.txt": """
        FOR doc IN mitre_cwe_vertex_collection
          FILTER doc._stix2arango_note == "version=4_15"
          AND IS_ARRAY(doc.external_references)
          AND doc.x_mitre_deprecated != true
          AND doc.revoked != true
          AND doc.type == "weakness"
          RETURN doc.name
    """,
    "mitre_capec_id_v3_9.txt": """
        FOR doc IN mitre_capec_vertex_collection
          FILTER doc._stix2arango_note == "version=3_9"
          AND doc.x_mitre_deprecated != true
          AND doc.revoked != true
          AND IS_ARRAY(doc.external_references)
          FOR reference IN doc.external_references
            FILTER reference.source_name == "capec"
            SORT reference.external_id ASC
            RETURN reference.external_id
    """,
    "mitre_capec_name_v3_9.txt": """
        FOR doc IN mitre_capec_vertex_collection
          FILTER doc._stix2arango_note == "version=3_9"
          AND doc.x_mitre_deprecated != true
          AND doc.revoked != true
          AND doc.type != "course-of-action"
          RETURN doc.name
    """,
    "mitre_attack_enterprise_id_v16_0.txt": """
        FOR doc IN mitre_attack_enterprise_vertex_collection
          FILTER doc._stix2arango_note == "version=16_0"
          AND doc.type != "x-mitre-matrix"
          AND doc.x_mitre_deprecated != true
          AND doc.revoked != true
          AND IS_ARRAY(doc.external_references)
          FOR reference IN doc.external_references
            FILTER reference.source_name == "mitre-attack"
            SORT reference.external_id ASC
            RETURN reference.external_id
    """,
    "mitre_attack_enterprise_name_v16_0.txt": """
        FOR doc IN mitre_attack_enterprise_vertex_collection
          FILTER doc._stix2arango_note == "version=16_0"
          AND doc.type != "x-mitre-matrix"
          AND doc.x_mitre_deprecated != true
          AND doc.revoked != true
          RETURN doc.name
    """,
    "mitre_attack_enterprise_aliases_v16_0.txt": """
        FOR alias IN UNIQUE(
          FLATTEN(
            FOR doc IN mitre_attack_enterprise_vertex_collection
              FILTER doc._stix2arango_note == "version=16_0"
              AND doc.type != "x-mitre-matrix"
              AND doc.x_mitre_deprecated != true
              AND doc.revoked != true
              AND IS_ARRAY(doc.x_mitre_aliases)
              RETURN doc.x_mitre_aliases
          )
        )
        RETURN alias
    """,
    "mitre_attack_ics_id_v16_0.txt": """
        FOR doc IN mitre_attack_ics_vertex_collection
          FILTER doc._stix2arango_note == "version=16_0"
          AND doc.type != "x-mitre-matrix"
          AND doc.x_mitre_deprecated != true
          AND doc.revoked != true
          AND IS_ARRAY(doc.external_references)
          FOR reference IN doc.external_references
            FILTER reference.source_name == "mitre-attack"
            SORT reference.external_id ASC
            RETURN reference.external_id
    """,
    "mitre_attack_ics_aliases_v16_0.txt": """
        FOR alias IN UNIQUE(
          FLATTEN(
            FOR doc IN mitre_attack_ics_vertex_collection
              FILTER doc._stix2arango_note == "version=16_0"
              AND doc.type != "x-mitre-matrix"
              AND doc.x_mitre_deprecated != true
              AND doc.revoked != true
              AND IS_ARRAY(doc.x_mitre_aliases)
              RETURN doc.x_mitre_aliases
          )
        )
        RETURN alias
    """,
    "mitre_attack_ics_name_v16_0.txt": """
        FOR doc IN mitre_attack_ics_vertex_collection
          FILTER doc._stix2arango_note == "version=16_0"
          AND doc.type != "x-mitre-matrix"
          AND doc.x_mitre_deprecated != true
          AND doc.revoked != true
          RETURN doc.name
    """,
    "mitre_attack_mobile_id_v16_0.txt": """
        FOR doc IN mitre_attack_mobile_vertex_collection
          FILTER doc._stix2arango_note == "version=16_0"
          AND doc.type != "x-mitre-matrix"
          AND doc.x_mitre_deprecated != true
          AND doc.revoked != true
          AND IS_ARRAY(doc.external_references)
          FOR reference IN doc.external_references
            FILTER reference.source_name == "mitre-attack"
            SORT reference.external_id ASC
            RETURN reference.external_id
    """,
    "mitre_attack_mobile_name_v16_0.txt": """
        FOR doc IN mitre_attack_mobile_vertex_collection
          FILTER doc._stix2arango_note == "version=16_0"
          AND doc.type != "x-mitre-matrix"
          AND doc.x_mitre_deprecated != true
          AND doc.revoked != true
          RETURN doc.name
    """,
    "mitre_atlas_id_v4_5_2.txt": """
        FOR doc IN mitre_atlas_vertex_collection
          FILTER doc._stix2arango_note == "version=4_5_2"
          AND doc.type != "x-mitre-matrix"
          AND doc.x_mitre_deprecated != true
          AND doc.revoked != true
          AND IS_ARRAY(doc.external_references)
          FOR reference IN doc.external_references
            FILTER reference.source_name == "mitre-atlas"
            SORT reference.external_id ASC
            RETURN reference.external_id
    """,
    "mitre_atlas_name_v4_5_2.txt": """
        FOR doc IN mitre_atlas_vertex_collection
          FILTER doc._stix2arango_note == "version=4_5_2"
          AND doc.type != "x-mitre-matrix"
          AND doc.x_mitre_deprecated != true
          AND doc.revoked != true
          RETURN doc.name
    """,
    "disarm_id_v1_5.txt": """
        FOR doc IN disarm_vertex_collection
          FILTER doc._stix2arango_note == "version=1_5"
          AND doc.type != "x-mitre-matrix"
          AND doc.x_mitre_deprecated != true
          AND doc.revoked != true
          AND IS_ARRAY(doc.external_references)
          FOR reference IN doc.external_references
            FILTER reference.source_name == "DISARM"
            SORT reference.external_id ASC
            RETURN reference.external_id
    """,
    "disarm_name_v1_5.txt": """
        FOR doc IN disarm_vertex_collection
          FILTER doc._stix2arango_note == "version=1_5"
          AND doc.type != "x-mitre-matrix"
          AND doc.x_mitre_deprecated != true
          AND doc.revoked != true
          RETURN doc.name
    """
}

# Execute each query and save the results in the script's directory
for filename, query in queries.items():
    cursor = db.aql.execute(query)
    results = [str(doc) for doc in cursor]
    
    # Full path for each output file
    filepath = os.path.join(script_dir, filename)
    
    # Write results to a text file with each result on a new line
    with open(filepath, 'w') as f:
        f.write("\n".join(results))
    
    print(f"Results saved to {filepath}")
