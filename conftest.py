import os
import pytest

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from config.config import Config


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")

    # Run headlessly in GitHub Actions
    if os.getenv("CI") == "true":
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(0)

    yield browser

    browser.quit()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, Config.EXPLICIT_WAIT)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        browser = item.funcargs.get("driver")

        if browser:
            os.makedirs("screenshots", exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = (
                f"screenshots/{item.name}_{timestamp}.png"
            )

            browser.save_screenshot(screenshot_path)
            print(f"Failure screenshot: {screenshot_path}")