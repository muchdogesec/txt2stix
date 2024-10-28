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
        return self._retrieve_objects(endpoint)
    
    def get_xxxx_objects(self, id, type):
        return self._retrieve_objects(urljoin(self.api_root, f"/api/v1/{type}/objects/{id}/"))
    
    def get_location_objects(self, id):
        return self._retrieve_objects(urljoin(self.api_root, f"/api/v1/location/objects/?alpha2_code={id}"))
    
    def _retrieve_objects(self, endpoint, key='objects'):
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
        if stix_mapping in ['location']:
            host = 'ctibutler'
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
                return retreiver.get_xxxx_objects(id, 'capec')
            case "mitre-atlas-id":
                return retreiver.get_xxxx_objects(id, 'atlas')
            case "mitre-cwe-id":
                return retreiver.get_xxxx_objects(id, 'cwe')
            case "cve-id":
                return retreiver.get_xxxx_objects(id, 'cve')
            case "cpe-id":
                return retreiver.get_xxxx_objects(id, 'cpe')
            case "location":
                return retreiver.get_location_objects(id)
            case _:
                raise NotImplementedError(f"pair {(host, stix_mapping)=} not implemented")
    except Exception as e:
        pass
    return None
