# ============================================================
# FILE: pages/login_page.py
# PURPOSE: This file represents the Login Page of saucedemo.com
#
# PAGE OBJECT MODEL (POM) EXPLAINED:
# Instead of writing locators (like username field, password field)
# directly inside your test, you put them here in a separate "page" file.
# This way, if the website changes a button, you only fix it in ONE place.
# ============================================================

from selenium.webdriver.common.by import By           # By helps us find elements (by ID, CSS, etc.)
from selenium.webdriver.support.ui import WebDriverWait  # WebDriverWait makes the test wait for elements to appear
from selenium.webdriver.support import expected_conditions as EC  # EC defines WHAT we're waiting for


class LoginPage:
    """
    This class represents the Login Page.
    It holds all the locators (how to find elements) and
    actions (what to do on the page) for login.
    """

    # --- LOCATORS ---
    # These tell Selenium HOW to find each element on the page.
    # We store them here as variables so we only define them once.

    URL = "https://www.saucedemo.com"  # The website URL

    USERNAME_FIELD = (By.ID, "user-name")       # The username input box
    PASSWORD_FIELD = (By.ID, "password")        # The password input box
    LOGIN_BUTTON   = (By.ID, "login-button")    # The login button
    ERROR_MESSAGE  = (By.CSS_SELECTOR, "[data-test='error']")  # The error message box (shown on failed login)

    # --- CONSTRUCTOR ---
    # When we create a LoginPage object, we pass in the browser (driver).
    def __init__(self, driver):
        self.driver = driver
        # WebDriverWait tells Selenium: "wait UP TO 10 seconds for elements to appear before giving up"
        self.wait = WebDriverWait(driver, 10)

    # --- ACTIONS ---
    # These are the things a user can DO on this page.

    def open(self):
        """Opens the saucedemo login page in the browser."""
        self.driver.get(self.URL)

    def enter_username(self, username):
        """Finds the username field and types the given username into it."""
        # wait.until means: keep waiting (up to 10s) until the element is visible on screen
        field = self.wait.until(EC.visibility_of_element_located(self.USERNAME_FIELD))
        field.clear()           # Clear any existing text first
        field.send_keys(username)  # Type the username

    def enter_password(self, password):
        """Finds the password field and types the given password into it."""
        field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        field.clear()
        field.send_keys(password)

    def click_login(self):
        """Clicks the Login button."""
        button = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        button.click()

    def login(self, username, password):
        """
        CONVENIENCE METHOD: Does the full login in one step.
        Calls enter_username, enter_password, and click_login together.
        Your tests will call this method instead of calling each step separately.
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self):
        """Reads and returns the error message text shown on a failed login."""
        error = self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        return error.text

    def is_error_displayed(self):
        """Returns True if an error message is visible, False if not."""
        try:
            self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return True
        except:
            return False
