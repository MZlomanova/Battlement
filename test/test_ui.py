import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from battlenet.ui.main_page import MainPage
from battlenet.ui.product_page import ProductPage
from battlenet.ui.constants import LANGUAGE_RU, LANGUAGE_EN


@allure.id("UI-1")
@allure.story("Проверка доступности сайта (открытие браузером)")
@allure.feature("READ")
@allure.severity("blocker")
def test_availability(driver: WebDriver):
    """
    Данная функция проверяет доступность ресурса (открывается ли он через
    браузер). Функция создает класс главной страницы и открывает ее.
    """
    main_page = MainPage(driver)
    main_page.open()

    assert len(main_page.get_recommended()) > 0
    assert len(main_page.get_featured()) > 0
    assert len(main_page.get_trending_now()) > 0
    assert len(main_page.get_most_gifted()) > 0


@allure.id("UI-2")
@allure.story("Проверка возможности изменения языка сайта")
@allure.feature("UPDATE")
@allure.severity("blocker")
def test_language_change(driver: WebDriver):
    """
    Данная функция позволяет изменить язык сайта. 
    Создает класс главной страницы и использует его методы для изменения языка
    """
    main_page = MainPage(driver)
    main_page.open()
    
    """
    Ниже функции проверки изменения языка:
    """
    assert driver.current_url.endswith(LANGUAGE_EN)

    main_page.set_language(LANGUAGE_RU)
    assert driver.current_url.endswith(LANGUAGE_RU)

    main_page.set_language(LANGUAGE_EN)
    assert driver.current_url.endswith(LANGUAGE_EN)


@allure.id("UI-3")
@allure.story("Проверка работоспособности поля поиск на главной странице")
@allure.feature("UPDATE")
@allure.severity("blocker")
def test_search(driver: WebDriver):
    """
    Эта функция создает класс главной страницы и используется для проверки поля
    поиска на главной странице сайта
    """
    main_page = MainPage(driver)
    main_page.open()

    search_results = main_page.get_search_results("warcraft")
    """
    Метод вводит в поле поиск название товара, который пробуем найти
    """

    assert len(search_results) > 0
    """
    Проверяет, что поиск отработал и вернул больше нуля результатов
    """


@allure.id("UI-4")
@allure.story("Проверка работоспособности выпадающего списка в поле поиск (выбор)")
@allure.feature("READ")
@allure.severity("critical")
@allure.severity("blocker")
def test_product_selection(driver: WebDriver):
    """
    Функция проверяет возможность выбора продукта на странице
    """
    main_page = MainPage(driver)
    main_page.open()

    search_results = main_page.get_search_results("war within")
    assert len(search_results) == 1
    """
    Метод открывает браузер, вводит в поле поиска war within
    и возвращает результат - найденный продукт
    """

    main_page.select_search_item(search_results[0])
    assert driver.current_url.endswith("world-of-warcraft-the-war-within")
    """
    Метод выбирает найденный продукт и проверяет, что осуествляется
    переход на страницу с продуктом
    """


@allure.id("UI-5")
@allure.story("Проверка доступности конкретного товара на странице")
@allure.feature("READ")
@allure.severity("blocker")
def test_product(driver: WebDriver):
    """
    Функция проверяет, что страница продукта, который искали, открывается
    """
    product_page = ProductPage(driver)
    product_page.open()
    assert True


@allure.id("UI-6")
@allure.story("Проверка возможности выбора пакета и изменения"
              + "информации на странице при выборе пакета")
@allure.feature("READ")
@allure.severity("blocker")
def test_product_options(driver: WebDriver):
    """
    Функция проверяет возможность выбора опций продукта (их 3),
    обновление информации на слайдере при изменении опции
    """
    product_page = ProductPage(driver)
    product_page.open()

    assert len(product_page.get_options()) == 3
    """
    Проверка количества доступных опций
    """

    product_page.set_option("Heroic")
    assert product_page.get_active_slide().get_attribute(
        "data-swiper-slide-index") == "6"
    """
    Проверка, что отображается описание опции Heroic
    """

    product_page.set_option("Epic")
    assert product_page.get_active_slide().get_attribute(
        "data-swiper-slide-index") == "1"
    """
    Проверка, что отображается описание опции Epic
    """
    product_page.set_option("Base")
    assert product_page.get_active_slide().get_attribute(
        "data-swiper-slide-index") == "7"
    """
    Проверка, что отображается описание опции Base
    """