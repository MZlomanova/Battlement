import numbers
from battlenet.api.bearer_auth import BearerAuth
from battlenet.api.constants import BATTLE_NET_AUTH_TEST_URL
from battlenet.api.achievement import Achievement
from battlenet.api.search import Search
import allure

@allure.id("API-1")
@allure.story("Получения токена авторизации)")
@allure.feature("GET")
@allure.severity("blocker")
def test_auth_token(bearer_auth: BearerAuth):
    """Функция отправляет запрос на проверку токена,
    в ответе приходит статус 200 и необходимые поля"""
    response = bearer_auth.test_token()
    body = response.json()

    assert response.status_code == 200
    assert isinstance(body["last_updated_timestamp"], numbers.Number)
    assert isinstance(body["price"], numbers.Number)
    assert body["_links"]["self"]["href"] == (
        BATTLE_NET_AUTH_TEST_URL
    )


@allure.id("API-2")
@allure.story("Получения списка достижений, доступных в игре")
@allure.feature("READ")
@allure.severity("blocker")
def test_categories(bearer_auth: BearerAuth):
    """
    Функиця проверяет доступность информации о
    категории достижений (ачивок) и что их количество больше 0
    """
    response = Achievement(bearer_auth).get_categories()
    categories = response.json()["categories"]

    assert response.status_code == 200
    assert len(categories) > 0


@allure.id("API-3")
@allure.story("Получение списка достижений конкретной категории )")
@allure.feature("READ")
@allure.severity("blocker")
def test_category(bearer_auth: BearerAuth):
    """
    Функция выгружает конкретную категорию достижений (ачивок)
    """
    response = Achievement(bearer_auth).get_category("14803")

    assert response.status_code == 200
    assert response.json()["id"] == 14803


@allure.id("API-4")
@allure.story("Запрос информации о несуществующей проверке,"
              + "негативная проверка")
@allure.feature("READ")
@allure.severity("blocker")
def test_category_not_found(bearer_auth: BearerAuth):
    """
    Функция проверяет систему на возврат ошибки при запросе
    несуществующей категории достижений
    """
    response = Achievement(bearer_auth).get_category("not-id")
    body = response.json()

    assert response.status_code == 404
    assert body["code"] == 404
    assert body["detail"] == "Not Found"


@allure.id("API-5")
@allure.story("Проверка ограничения прав у неавторизованного пользователя")
@allure.feature("READ")
@allure.severity("blocker")
def test_categories_not_authorized():
    """
    Функция провяет, что списки достижений не
    доступны неавторизованному пользователю (безопасность)
    """
    response = Achievement(None).get_categories()
    assert response.status_code == 401


@allure.id("API-6")
@allure.story("Проверка работоспособности поля поиск через API")
@allure.feature("READ")
@allure.severity("blocker")
def test_search():
    """
    Функция проверяет работоспособность поля поиск на сайте через API
    """
    response = Search().perform("warcraft")

    assert response.status_code == 200
    assert len(response.json()) > 0


@allure.id("API-7")
@allure.story("Проверка пустоты в поле поиск")
@allure.feature("READ")
@allure.severity("blocker")
def test_search_empty():
    """
    Функция проверяет пустоту: в поле поиск не введены данные.
    В ответе приходит пустота.
    """
    response = Search().perform("")

    assert response.status_code == 200
    assert len(response.json()) == 0


@allure.id("API-8")
@allure.story("Проверка поля поиск без указания региона для поиска")
@allure.feature("READ")
@allure.severity("blocker")
def test_search_no_locale():
    """
    Функция проверяет поиск без локализации - не указан регион.
    В ответе приходит ошибка, статус код 400
    """
    response = Search().perform("warcraft", None)
    body = response.json()

    assert response.status_code == 400
    assert body["error"] == "Bad Request"
    assert body["status"] == 400


@allure.id("API-9")
@allure.story("Проверка поля поиск с указанием несуествующего региона,"
              + "негативная проверка")
@allure.feature("READ")
@allure.severity("blocker")
def test_search_wrong_locale():
    """
    Фунция проверяет поиск с указанием несуществующей локализации.
    В ответе должна приходить ошибка - статус код 400
    """
    response = Search().perform("warcraft", "zz-ZZ")

    assert response.status_code == 400
    assert len(response.json()) == 0
