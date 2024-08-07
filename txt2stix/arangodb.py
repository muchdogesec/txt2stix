from arango import ArangoClient
import dotenv, json, os
import stix2

dotenv.load_dotenv()


class ArangoSession:
    ATTACK_ID_TABLES = {
        "mitre-attack-ics-id": "mitre_attack_ics_vertex_collection",
        "mitre-attack-mobile-id": "mitre_attack_mobile_vertex_collection",
        "mitre-attack-enterprise-id": "mitre_attack_enterprise_vertex_collection",
    }

    def __init__(self) -> None:
        host_url, db_name, user, passwd = (
            os.environ["ARANGODB_HOST_URL"],
            os.environ["ARANGODB_DATABASE"],
            os.environ["ARANGODB_USERNAME"],
            os.environ["ARANGODB_PASSWORD"],
        )
        self.client = ArangoClient(hosts=host_url)
        self.db = self.client.db(db_name, username=user, password=passwd)

    def mitre_attack_id(self, id, stix_mapping):
        table = self.ATTACK_ID_TABLES[stix_mapping]
        cursor = self.db.aql.execute(
            f"""
        FOR doc IN {table}
            FILTER IS_ARRAY(doc.external_references)
            FOR external_references IN doc.external_references
                FILTER external_references.external_id == @id
            RETURN KEEP(doc, KEYS(doc, true))
        """,
            bind_vars=dict(id=id),
        )
        return self.to_stix_observables(cursor)

    def mitre_capec_id(self, id):
        cursor = self.db.aql.execute(
            """
        FOR doc IN mitre_capec_vertex_collection
            FILTER doc.type == 'attack-pattern' AND IS_ARRAY(doc.external_references)
            FOR external_references IN doc.external_references
                FILTER external_references.external_id == @id
            RETURN KEEP(doc, KEYS(doc, true))
        """,
            bind_vars=dict(id=id),
        )
        return self.to_stix_observables(cursor)

    def mitre_cwe_id(self, id):
        cursor = self.db.aql.execute(
            """
        FOR doc IN mitre_cwe_vertex_collection
            FILTER doc.type == 'weakness' AND IS_ARRAY(doc.external_references)
            FOR external_references IN doc.external_references
                FILTER external_references.external_id == @id
                RETURN KEEP(doc, KEYS(doc, true))
        """,
            bind_vars=dict(id=id),
        )
        return self.to_stix_observables(cursor)

    def cve_id(self, id):
        cursor = self.db.aql.execute(
            """
        FOR doc IN nvd_cve_vertex_collection
            FILTER doc.type == 'vulnerability'
            AND doc.name == @id
            RETURN KEEP(doc, KEYS(doc, true))
        """,
            bind_vars=dict(id=id),
        )
        return self.to_stix_observables(cursor)

    def cpe_id(self, id):
        cursor = self.db.aql.execute(
            """
        FOR doc IN nvd_cpe_vertex_collection
            FILTER doc.type == 'software'
            AND doc.cpe == @id
            RETURN KEEP(doc, KEYS(doc, true))
        """,
            bind_vars=dict(id=id),
        )
        return self.to_stix_observables(cursor)

    def to_stix_observables(self, cursor):
        sdos = []
        for item in cursor:
            sdos.append(stix2.parse(item, allow_custom=True))
        return sdos


if __name__ == "__main__":
    session = ArangoSession()
    attack_ids = session.mitre_attack_id("M0948", "mitre-attack-ics-id")
    capec_ids = session.mitre_capec_id("CAPEC-1")
    cwes = session.mitre_cwe_id("CWE-276")
    cpes = session.cpe_id(
        "cpe:2.3:a:wpeka:wp_cookie_consent:2.2.9:*:*:*:-:wordpress:*:*"
    )
    cves = session.cve_id("CVE-2001-0308")
    print(attack_ids, capec_ids, cwes, cpes, cves)
    print("done")
