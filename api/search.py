import requests
from battlenet.api.constants import BATTLE_NET_SHOP_URL


class Search:
    def __init__(self, url=BATTLE_NET_SHOP_URL):
        self._url = url

    def perform(self, str, locale="en-US"):
        params = {
            "q": str,
            "l": locale
        }
        return requests.get(self._url + "/api/search", params=params)
