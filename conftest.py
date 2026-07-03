# ============================================================
# FILE: conftest.py
# PURPOSE: Browser setup and teardown for ALL tests
#
# WHAT IS conftest.py?
# This is a special pytest file. pytest automatically reads it
# before running any tests. It sets up shared "fixtures" —
# think of fixtures as reusable setup steps that every test can use.
#
# In our case: every test needs a browser. Instead of opening
# and closing the browser inside each test file, we do it ONCE
# here and share it across all tests.
# ============================================================
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config.config_reader import get_config
from api.api_client import APIClient


@pytest.fixture()
def driver():
    """
    FIXTURE: driver
    ---------------
    This fixture:
    1. Opens a Chrome browser before each test
    2. Passes the browser to the test (via the 'driver' parameter)
    3. Closes the browser after each test finishes (even if the test fails)
    Any test that has 'driver' as a parameter will automatically
    use this fixture. You'll see this in the test file.

    CI vs LOCAL:
    GitHub Actions runners have no display (no screen), so Chrome must
    run in "headless" mode there, with a couple of extra flags
    (--no-sandbox, --disable-dev-shm-usage) that Chrome needs to start
    up cleanly inside a container. Locally on your Mac, none of this
    is needed - you'll still see the actual browser window as before.

    GitHub Actions automatically sets an environment variable CI=true
    on every run, so we use that to detect where we're running.
    """
    print("\n🌐 Opening Chrome browser...")

    options = Options()

    is_ci = os.getenv("CI", "false").lower() == "true"
    if is_ci:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

    # ChromeDriverManager automatically downloads the correct
    # version of ChromeDriver for your Chrome browser.
    # You don't need to download anything manually.
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Maximise the browser window so elements are fully visible
    # (skipped in headless CI mode since --window-size handles it there)
    if not is_ci:
        driver.maximize_window()

    # 'yield' means: "pause here, run the test, then come back"
    # Everything ABOVE yield = setup (runs before the test)
    # Everything BELOW yield = teardown (runs after the test)
    yield driver
    # --- TEARDOWN ---
    # This runs after every test, whether it passed or failed.
    print("\n🔒 Closing browser...")
    driver.quit()  # Close the browser completely


@pytest.fixture(scope="session")
def api_client():
    """
    FIXTURE: api_client
    --------------------
    This fixture is for API tests, not UI tests — it does NOT open
    a browser. It reads the API base URL from config/config.yaml
    and hands back a ready-to-use APIClient (a thin wrapper around
    the 'requests' library).

    scope="session" means this fixture is created ONCE for the
    whole test run and reused across every API test, instead of
    being recreated per test — API tests don't need a fresh
    browser-like setup each time, so this keeps things fast.
    """
    config = get_config()
    return APIClient(config["api_base_url"])