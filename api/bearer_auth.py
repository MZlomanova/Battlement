import requests
from battlenet.api.constants import BATTLE_NET_AUTH_TEST_URL


# https://stackoverflow.com/a/58055668
class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

    # https://develop.battle.net/documentation/guides/getting-started
    def test_token(self):
        return requests.get(
            BATTLE_NET_AUTH_TEST_URL,
            auth=self
        )
