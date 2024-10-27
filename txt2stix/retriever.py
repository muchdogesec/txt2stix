from urllib.parse import urljoin
import dotenv, os
import stix2
import requests

dotenv.load_dotenv()


class STIXObjectRetriever:
    api_root = os.environ['CTIBUTLER_HOST']
    api_key = os.environ['CTIBUTLER_HOST']

    def __init__(self, host="ctibutler") -> None:
        if host == "ctibutler":
            self.api_root = os.environ['CTIBUTLER_HOST']
            self.api_key = os.environ['CTIBUTLER_APIKEY']
        elif host == "vulmatch":
            self.api_root = os.environ['VULMATCH_HOST']
            self.api_key = os.environ['VULMATCH_APIKEY']
        else:
            raise NotImplementedError("The type `%s` is not supported", host)

    def get_attack_objects(self, matrix, attack_id):
        endpoint = urljoin(self.api_root, f"/api/v1/attack-{matrix}/objects/{attack_id}/")
        return self.get_objects(endpoint)
    
    def get_capec_object(self, capec_id):
        return self.get_objects(urljoin(self.api_root, f"/api/v1/capec/objects/{capec_id}/"))
    
    def get_cwe_object(self, cwe_id):
        return self.get_objects(urljoin(self.api_root, f"/api/v1/cwe/objects/{cwe_id}/"))
    
    def get_cve_object(self, cve_id):
        return self.get_objects(urljoin(self.api_root, f"/api/v1/cve/objects/{cve_id}/"), 'vulnerabilities')
    
    def get_cpe_object(self, cpe_id):
        return self.get_objects(urljoin(self.api_root, f"/api/v1/cpe/objects/{cpe_id}/"))
    
    def get_objects(self, endpoint, key='objects'):
        s = requests.Session()
        s.headers.update({
            "Authority": f"Bearer {self.api_key}"
        })
        data = []
        page = 1
        while True:
            resp = s.get(endpoint, params=dict(page=page, page_size=1000))
            if resp.status_code != 200:
                break
            d = resp.json()
            if len(d[key]) == 0:
                break
            data.extend(d[key])
            page+=1
            if d['page_results_count'] < d['page_size']:
                break
        return data
    
def retrieve_stix_objects(stix_mapping: str, id, host=None):
    try:
        if not host:
            host, stix_mapping = stix_mapping.split('-', 1)
        retreiver = STIXObjectRetriever(host)
        match stix_mapping:
            case 'mitre-attack-ics-id':
                return retreiver.get_attack_objects('ics', id)
            case 'mitre-attack-mobile-id':
                return retreiver.get_attack_objects('mobile', id)
            case 'mitre-attack-enterprise-id':
                return retreiver.get_attack_objects('enterprise', id)
            case "mitre-capec-id":
                return retreiver.get_capec_object(id)
            case "mitre-cwe-id":
                return retreiver.get_cwe_object(id)
            case "cve-id":
                return retreiver.get_cve_object(id)
            case "cpe-id":
                return retreiver.get_cpe_object(id)
            case _:
                raise NotImplementedError(f"pair {(host, stix_mapping)=} not implemented")
    except Exception as e:
        pass
    return None
