# ============================================================
# FILE: tests/test_login.py
# PURPOSE: All login test scenarios for saucedemo.com
#
# HOW THIS WORKS WITH POM:
# - We import LoginPage from the pages folder
# - We create a LoginPage object and pass it the browser (driver)
# - We call the methods we defined in login_page.py
# - We never touch raw Selenium commands here — the page object handles that
#
# VALID TEST CREDENTIALS FOR SAUCEDEMO.COM:
#   Username: standard_user       Password: secret_sauce  → Should PASS
#   Username: locked_out_user     Password: secret_sauce  → Should FAIL (locked)
#   Username: wrong_user          Password: wrong_pass    → Should FAIL (invalid)
# ============================================================

import pytest
from pages.login_page import LoginPage  # Import our Page Object


# ============================================================
# TEST 1: Successful Login
# SCENARIO: Valid username and password → user lands on products page
# ============================================================
def test_successful_login(driver):
    """
    GIVEN I am on the saucedemo login page
    WHEN  I enter valid credentials (standard_user / secret_sauce)
    THEN  I should be redirected to the products page
    """

    # Step 1: Create a LoginPage object, passing in the browser
    login_page = LoginPage(driver)

    # Step 2: Open the login page in the browser
    login_page.open()

    # Step 3: Perform the login using our page object method
    login_page.login("standard_user", "secret_sauce")

    # Step 4: ASSERT — Check the result is what we expected
    # After successful login, the URL should contain "/inventory.html"
    current_url = driver.current_url
    assert "/inventory.html" in current_url, (
        f"Expected to land on inventory page but got: {current_url}"
    )

    print("✅ TEST PASSED: Successful login works correctly")


# ============================================================
# TEST 2: Login with Wrong Password
# SCENARIO: Valid username but wrong password → error message appears
# ============================================================
def test_login_with_wrong_password(driver):
    """
    GIVEN I am on the saucedemo login page
    WHEN  I enter a valid username but wrong password
    THEN  I should see an error message
    AND   I should NOT be redirected away from the login page
    """

    login_page = LoginPage(driver)
    login_page.open()

    # Use a valid username but wrong password
    login_page.login("standard_user", "wrong_password_123")

    # Assert that an error message is shown
    assert login_page.is_error_displayed(), (
        "Expected an error message to appear but none was found"
    )

    # Assert the error message contains the expected text
    error_text = login_page.get_error_message()
    assert "Username and password do not match" in error_text, (
        f"Unexpected error message: {error_text}"
    )

    print(f"✅ TEST PASSED: Correct error shown → '{error_text}'")


# ============================================================
# TEST 3: Login with Locked Out User
# SCENARIO: Locked account → specific error message appears
# ============================================================
def test_locked_out_user(driver):
    """
    GIVEN I am on the saucedemo login page
    WHEN  I log in with a locked-out account (locked_out_user)
    THEN  I should see a 'locked out' error message
    """

    login_page = LoginPage(driver)
    login_page.open()

    login_page.login("locked_out_user", "secret_sauce")

    # Assert error is displayed
    assert login_page.is_error_displayed(), (
        "Expected a locked-out error message but none appeared"
    )

    error_text = login_page.get_error_message()
    assert "locked out" in error_text.lower(), (
        f"Expected locked out message but got: {error_text}"
    )

    print(f"✅ TEST PASSED: Locked user correctly blocked → '{error_text}'")


# ============================================================
# TEST 4: Login with Empty Fields
# SCENARIO: Submit with no username or password → error message appears
# ============================================================
def test_login_with_empty_fields(driver):
    """
    GIVEN I am on the saucedemo login page
    WHEN  I click Login without entering any credentials
    THEN  I should see a validation error message
    """

    login_page = LoginPage(driver)
    login_page.open()

    # Click login without entering anything
    login_page.click_login()

    # Assert error is shown
    assert login_page.is_error_displayed(), (
        "Expected a validation error for empty fields but none appeared"
    )

    error_text = login_page.get_error_message()
    assert "Username is required" in error_text, (
        f"Unexpected error message: {error_text}"
    )

    print(f"✅ TEST PASSED: Empty field validation works → '{error_text}'")


# ============================================================
# BONUS: Parametrized Test
# Run the same test with multiple sets of data in one go.
# This is a more advanced pytest feature — shows you know pytest well.
# ============================================================
@pytest.mark.parametrize("username, password, expected_error", [
    ("",              "secret_sauce",  "Username is required"),
    ("standard_user", "",             "Password is required"),
    ("wrong_user",    "wrong_pass",   "Username and password do not match"),
])
def test_login_validation_scenarios(driver, username, password, expected_error):
    """
    PARAMETRIZED TEST: Runs 3 times automatically with different data.
    This single test replaces 3 separate test functions.
    Shows recruiters you know how to write data-driven tests.
    """

    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(username, password)

    assert login_page.is_error_displayed(), "Expected error message not found"

    error_text = login_page.get_error_message()
    assert expected_error in error_text, (
        f"Expected '{expected_error}' but got '{error_text}'"
    )

    print(f"✅ PASSED: username='{username}' → '{error_text}'")
