import requests
from battlenet.api.constants import BATTLE_NET_API_URL


class Achievement:
    def __init__(self,
                 auth,
                 api_url=BATTLE_NET_API_URL,
                 namespace="static-us",
                 region="us"):
        self._api_url = api_url
        self._auth = auth
        self._params = {
            "namespace": namespace,
            "region": region
        }

    def get_categories(self):
        return requests.get(self._api_url
                            + "/data/wow/achievement-category/index",
                            auth=self._auth,
                            params=self._params)

    def get_category(self, category_id: str):
        return requests.get(self._api_url
                            + "/data/wow/achievement-category/"
                            + category_id,
                            auth=self._auth,
                            params=self._params)
