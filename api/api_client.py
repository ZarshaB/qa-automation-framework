"""
Thin wrapper around requests, so tests call self.client.get(...) instead of
requests.get(...) directly. This is the pattern most real frameworks use:
it gives you one place to add auth headers, logging, or retries later
without touching every test.
"""

import requests


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def get(self, endpoint: str, params: dict = None, **kwargs):
        return self.session.get(f"{self.base_url}{endpoint}", params=params, **kwargs)

    def post(self, endpoint: str, json: dict = None, **kwargs):
        return self.session.post(f"{self.base_url}{endpoint}", json=json, **kwargs)

    def put(self, endpoint: str, json: dict = None, **kwargs):
        return self.session.put(f"{self.base_url}{endpoint}", json=json, **kwargs)

    def patch(self, endpoint: str, json: dict = None, **kwargs):
        return self.session.patch(f"{self.base_url}{endpoint}", json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self.session.delete(f"{self.base_url}{endpoint}", **kwargs)
