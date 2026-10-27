from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config.config import Config


class LoginPage:
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def open(self):
        self.driver.get(Config.BASE_URL)

    def login(self, username, password):
        self.wait.until(
            EC.visibility_of_element_located(self.USERNAME)
        ).send_keys(username)

        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_error_message(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE)
        ).text