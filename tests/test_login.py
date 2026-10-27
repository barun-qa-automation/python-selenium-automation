import pytest

from config.config import Config
from pages.login_page import LoginPage
from pages.products_page import ProductsPage


def test_valid_login(driver, wait):
    login_page = LoginPage(driver, wait)
    products_page = ProductsPage(driver, wait)

    login_page.open()
    login_page.login(
        Config.VALID_USERNAME,
        Config.VALID_PASSWORD
    )

    assert products_page.get_title() == "Products"


@pytest.mark.parametrize(
    "username, password",
    [
        ("invalid_user", "wrong_password"),
        ("standard_user", "wrong_password"),
        ("", ""),
    ],
)
def test_invalid_login(driver, wait, username, password):
    login_page = LoginPage(driver, wait)

    login_page.open()
    login_page.login(username, password)

    error = login_page.get_error_message()

    assert "Epic sadface" in error