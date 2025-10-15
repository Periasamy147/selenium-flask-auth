import os
import pytest
import psycopg2
from testing.selenium_helper import (
    init_driver,
    delete_user,
    register,
    login,
    init_test_db,
    dashboard,
    logout
)

# Initialize DB before all tests
init_test_db()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/flask_db"
)
TEST_USER = "TestUser"
TEST_PASS = "SecurePass123"


@pytest.fixture(scope="module")
def driver_wait():
    driver, wait = init_driver()
    yield driver, wait
    driver.quit()


def test_register_new_user(driver_wait):
    driver, wait = driver_wait
    delete_user(TEST_USER)
    result = register(driver, wait, TEST_USER, TEST_PASS)
    assert result, "New user should register successfully"


def test_login_valid_user(driver_wait):
    driver, wait = driver_wait
    result = login(driver, wait, TEST_USER, TEST_PASS)
    assert result, "Valid user should log in successfully"


def test_wrong_login_password(driver_wait):
    driver, wait = driver_wait
    result = login(driver, wait, TEST_USER, "WrongPass")
    assert not result, "Login should fail with wrong password"


def test_no_user_login(driver_wait):
    driver, wait = driver_wait
    result = login(driver, wait, "NotTheUser", "NotThePassword")
    assert not result, "Login should fail for non-existing user"


def test_register_existing_user(driver_wait):
    driver, wait = driver_wait
    result = register(driver, wait, TEST_USER, TEST_PASS)
    assert not result, "Register should fail for existing user"


def test_register_empty_fields(driver_wait):
    driver, wait = driver_wait
    delete_user("")
    result = register(driver, wait, "", "")
    assert not result, "Register should fail for empty fields"


def test_register_long_input(driver_wait):
    driver, wait = driver_wait
    long_username = "U" * 300
    long_password = "P" * 300
    delete_user(long_username)
    result = register(driver, wait, long_username, long_password)
    assert not result, "Register should fail for extremely long inputs"


# def test_direct_dashboard_access(driver_wait):
#     driver, wait = driver_wait
#     url_after = dashboard(driver)
#     assert "/login" in url_after or "Login" in driver.page_source, \
#         "Unauthenticated user should be redirected to login, not see dashboard"
