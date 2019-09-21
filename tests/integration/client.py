import requests
from tenacity import retry, retry_if_exception_type, stop_after_delay, wait_fixed


class API:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
        self.users = ResourceCollection(self, "users")
        self.artists = ResourceCollection(self, "artists")
        self.venues = ResourceCollection(self, "venues")

    @retry(
        retry=retry_if_exception_type(
            (requests.exceptions.ConnectionError, requests.exceptions.HTTPError)
        ),
        stop=stop_after_delay(10),
        wait=wait_fixed(1),
        reraise=True,
    )
    def wait(self):
        return requests.head(self.base_url).raise_for_status()

    def authenticate(self, username, password):
        response = requests.post(f"{self.base_url}/tokens", auth=(username, password))
        response.raise_for_status()
        assert response.status_code == 201
        self.token = response.json()["token"]


class ResourceCollection:
    def __init__(self, api, path):
        self.api = api
        self.path = path

    @property
    def url(self):
        return f"{self.api.base_url}/{self.path}"

    @property
    def headers(self):
        if self.api.token is None:
            return {}
        return {"Authorization": f"Bearer {self.api.token}"}

    def list(self):
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()
        assert response.status_code == 200
        return response.json()

    def get(self, resource_id):
        response = requests.get(f"{self.url}/{resource_id}", headers=self.headers)
        response.raise_for_status()
        assert response.status_code == 200
        return response.json()

    def create(self, data):
        response = requests.post(self.url, json=data, headers=self.headers)
        response.raise_for_status()
        assert response.status_code == 201
        return response.json()

    def update(self, resource_id, data):
        response = requests.put(
            f"{self.url}/{resource_id}", json=data, headers=self.headers
        )
        response.raise_for_status()
        assert response.status_code == 200
        return response.json()

    def delete(self, resource_id):
        response = requests.delete(f"{self.url}/{resource_id}", headers=self.headers)
        response.raise_for_status()
        assert response.status_code == 204
