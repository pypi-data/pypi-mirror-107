import requests
import warnings
from .exceptions import CredentialsException, SignalBoxException
from .client_functions import construct_user, construct_event, get, post, put

class Configuration:
    def __init__(self, host='localhost', port=5001, protocol='https'):
        self.host = host
        self.port = port
        self.protocol = protocol
        if "localhost" in host:
            warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made to host")

    def base_url(self):
        return f'{self.protocol}://{self.host}:{self.port}'

class Credentials:
    def __init__(self, api_key = None, access_token = None):
        self.api_key = api_key
        self.access_token = access_token
        if api_key is None and access_token is None:
            raise CredentialsException("one of api_key or access_token must not be null")

    def fetch_token(self, configuration: Configuration):
        if self.access_token is None:
            api_endpoint = f'{configuration.base_url()}/api/apikeys/exchange'
            api_headers = {"Content-Type": "application/json"}
            json_params = {  
                "apiKey": self.api_key,
            }

            r = requests.post(url = api_endpoint, json = json_params, headers = api_headers, verify=False)

            if r.ok:
                self.access_token = r.json()['access_token']
                if self.access_token == None:
                    raise CredentialsException("Access Token is None")

            else:
                raise CredentialsException(f'Server returned: {r.status_code}, with body: {r.text}')
        return self.access_token


class SignalBoxClient:
    def __init__(self, credentials: Credentials, configuration: Configuration = None):
        if configuration is None:
            configuration = Configuration()
        self.access_token = credentials.fetch_token(configuration=configuration)
        self.base_url = configuration.base_url()
        

    def create_offer(self, name: str, currency: str, price: float, cost: float):
        json_params = {
            "name": name,
            "currency": currency,
            "price": price,
            "cost": cost
        }
                    
        r = post(f'{self.base_url}/api/offers', json_params, self.access_token)
        if r.ok:
            return r.json()
        else:
            raise SignalBoxException(r.text)

    def create_user(self, name: str, commonUserId: str):
        json_params = {
            "name": name,
            "commonUserId": commonUserId
        }
        r = post(f'{self.base_url}/api/trackedUsers', json_params, self.access_token)
        if r.ok:
            return r.json()
        else:
            raise SignalBoxException(r.text)
    
    def create_or_update_users(self, users):
        for u in users:
            if 'commonUserId' not in u:
                raise Exception("Tracked Users require a common user Id")

        json_params = {
            "users": users
        }
        r = put(f'{self.base_url}/api/trackedUsers', json_params, self.access_token)

        if r.ok:
            return r.json()
        else:
            raise SignalBoxException(r.text)

    def create_segment(self, name: str):
        json_params = {
            "name": name
        }
        r = post(f'{self.base_url}/api/segments', json_params, self.access_token)

        if r.ok:
            return r.json()
        else:
            raise SignalBoxException(r.text)

    def create_experiment(self, offerIds: list, name: str, concurrentOffers: int = 1, segmentId: str = None):
        json_params = {
            "offerIds": offerIds,
            "segmentId": segmentId,
            "name": name,
            "concurrentOffers": concurrentOffers
        }
        r = post(f'{self.base_url}/api/experiments', json_params, self.access_token)
        if r.ok:
            return r.json()
        else:
            raise Exception(r.text)

    def get_experiment(self, experimentId: str):
        r = get(f'{self.base_url}/api/experiments/{experimentId}', self.access_token)

        if r.ok:
            return r.json()
        else:
            raise SignalBoxException(r.text)

    def recommend_offer(self, experimentId: str, commonUserId: str, features: dict = None):
        json_params = {
            "commonUserId" : commonUserId,
            "features": features
        }
        r = post(f'{self.base_url}/api/experiments/{experimentId}/recommendation', json_params, self.access_token)

        if r.ok:
            return r.json()
        else:
            raise SignalBoxException(r.text)

    def track_recommendation_outcome(self, recommendation, offerId, outcome):
        json_params = {
            "commonUserId" :  recommendation['commonUserId'],
            'experimentId': recommendation['experimentId'],
            'iterationId': recommendation['iterationId'],
            'recommendationId': recommendation['recommendationId'],
            'offerId': offerId,
            'outcome': outcome
        }
        r = post(f'{self.base_url}/api/experiments/{recommendation["experimentId"]}/outcome', json_params, self.access_token)

        if r.ok:
            return r.json()
        else:
            raise SignalBoxException(r.text)

    def construct_event(self, commonUserId, event_id, event_type, kind, properties, timestamp = None, source_system_id = None ):
        return construct_event(commonUserId, event_id, event_type, kind, properties, timestamp, source_system_id)
    
    def construct_user(self, commonUserId: str, name: str = None, properties: str = None):
        return construct_user(commonUserId, name=name, properties=properties)
    
    def log_events(self, events):
        r = post(f'{self.base_url}/api/events', events, self.access_token)
        if(r.ok):
            return r.json()
        else:
            raise SignalBoxException(r.text)
