import logging
from urllib.parse import urljoin
import dotenv, os
import stix2
import requests

dotenv.load_dotenv()


class STIXObjectRetriever:
    def __init__(self, host="ctibutler") -> None:
        if host == "ctibutler":
            self.api_root = os.environ['CTIBUTLER_BASE_URL'] + '/'
            self.api_key = os.environ.get('CTIBUTLER_API_KEY')
        elif host == "vulmatch":
            self.api_root = os.environ['VULMATCH_BASE_URL'] + '/'
            self.api_key = os.environ.get('VULMATCH_API_KEY')
        else:
            raise NotImplementedError("The type `%s` is not supported", host)

    def get_attack_object(self, matrix, attack_id):
        endpoint = urljoin(self.api_root, f"v1/attack-{matrix}/objects/{attack_id}/")
        return self._retrieve_objects(endpoint)
    
    def get_attack_objects(self, matrix, attack_ids):
        endpoint = urljoin(self.api_root, f"v1/attack-{matrix}/objects/?attack_id={','.join(attack_ids)}")
        return self._retrieve_objects(endpoint)
    
    def get_objects_by_id(self, id, type):
        return self._retrieve_objects(urljoin(self.api_root, f"v1/{type}/objects/{id}/"))
    
    def get_location_objects(self, id):
        return self._retrieve_objects(urljoin(self.api_root, f"v1/location/objects/?alpha2_code={id}"))
    
    def get_objects_by_name(self, name, type):
        return self._retrieve_objects(urljoin(self.api_root, f"v1/{type}/objects/?name={name}"))
    
    def get_objects_by_alias(self, alias, type):
        return self._retrieve_objects(urljoin(self.api_root, f"v1/{type}/objects/?alias={alias}"))
    
    def _retrieve_objects(self, endpoint, key='objects'):
        s = requests.Session()
        s.headers.update({
            "API-KEY": self.api_key,
        })
        data = []
        page = 1
        while True:
            resp = s.get(endpoint, params=dict(page=page, page_size=50))
            resp.raise_for_status()
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
        object_path = stix_mapping
        if stix_mapping in ['location']:
            host = 'ctibutler'
        if not host:
            host, object_path = stix_mapping.split('-', 1)
        retreiver = STIXObjectRetriever(host)
        match object_path:
            ### ATT&CK by ID
            case 'mitre-attack-ics-id':
                return retreiver.get_attack_object('ics', id)
            case 'mitre-attack-mobile-id':
                return retreiver.get_attack_object('mobile', id)
            case 'mitre-attack-enterprise-id':
                return retreiver.get_attack_object('enterprise', id)
            
            ### Others by ID
            case "mitre-capec-id":
                return retreiver.get_objects_by_id(id, 'capec')
            case "mitre-atlas-id":
                return retreiver.get_objects_by_id(id, 'atlas')
            case "disarm-id":
                return retreiver.get_objects_by_id(id, 'disarm')
            case "mitre-cwe-id":
                return retreiver.get_objects_by_id(id, 'cwe')
            case "cve-id":
                return retreiver.get_objects_by_id(id, 'cve')
            case "cpe-id":
                return retreiver.get_objects_by_id(id, 'cpe')
            case "location":
                return retreiver.get_location_objects(id)
            
            ### ATT&CK by Name
            case "mitre-attack-enterprise-name":
                return retreiver.get_objects_by_name(id, 'attack-enterprise')
            case "mitre-attack-mobile-name":
                return retreiver.get_objects_by_name(id, 'attack-mobile')
            case "mitre-attack-ics-name":
                return retreiver.get_objects_by_name(id, 'attack-ics')
            
            ### ATT&CK by Alias
            case "mitre-attack-enterprise-aliases":
                return retreiver.get_objects_by_alias(id, 'attack-enterprise')
            case "mitre-attack-mobile-aliases":
                return retreiver.get_objects_by_alias(id, 'attack-mobile')
            case "mitre-attack-ics-aliases":
                return retreiver.get_objects_by_alias(id, 'attack-ics')
            
            ### OTHERS by Name
            case "mitre-capec-name":
                return retreiver.get_objects_by_name(id, 'capec')
            case "mitre-cwe-name":
                return retreiver.get_objects_by_name(id, 'cwe')
            case "mitre-atlas-name":
                return retreiver.get_objects_by_name(id, 'atlas')
            case "disarm-name":
                return retreiver.get_objects_by_name(id, 'disarm')
            case _:
                raise NotImplementedError(f"pair {(host, object_path)=} not implemented")
    except (NotImplementedError, ValueError):
        pass
    except Exception as e:
        msg = f"failed to get {object_path} for {id} from {host}"
        logging.info(msg)
        logging.debug(msg, exc_info=True)
    return None
