import pytest
import requests
from selenium import webdriver
from battlenet.api.bearer_auth import BearerAuth
from battlenet.api.constants import (
    CLIENT_ID,
    CLIENT_SECRET,
    BATTLE_NET_AUTH_URL)


@pytest.fixture
def bearer_auth(client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                auth_url=BATTLE_NET_AUTH_URL):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(
        url=auth_url,
        headers=headers,
        auth=(client_id, client_secret),
        data=data
    )
    return BearerAuth(response.json()["access_token"])


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()
