"""
Step definitions for features/login.feature.

This reuses your EXISTING LoginPage POM class - the BDD layer is just a
different way of triggering the same page object methods you already wrote.
That's the point: BDD doesn't replace POM, it sits on top of it.
"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from pages.login_page import LoginPage

pytestmark = pytest.mark.bdd

# Points pytest-bdd at the feature file, relative to this file's location.
scenarios("../features/login.feature")


@pytest.fixture
def login_page(driver):
    """
    Uses your driver fixture from conftest.py, then opens the login page
    via LoginPage.open() - keeping navigation logic inside the page object
    where it belongs, rather than duplicating the URL here.
    """
    page = LoginPage(driver)
    page.open()
    return page


@given("I am on the SauceDemo login page")
def on_login_page(login_page):
    # Navigation already happens in the login_page fixture above.
    pass


@when(parsers.re(r'I log in with username "(?P<username>.*)" and password "(?P<password>.*)"'))
def perform_login(login_page, username, password):
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login()


@then("I should be redirected to the inventory page")
def assert_redirected_to_inventory(login_page, driver):
    assert "inventory" in driver.current_url

@then(parsers.parse('I should see the error message "{expected_error}"'))
def assert_error_message(login_page, expected_error):
    actual_error = login_page.get_error_message()
    assert expected_error in actual_error, (
        f"Expected error containing '{expected_error}', got '{actual_error}'"
    )