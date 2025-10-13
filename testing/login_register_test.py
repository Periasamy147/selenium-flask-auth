import pytest
import psycopg2
import os
from testing.selenium_helper import init_driver, register, login, dashboard

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/flask_db")
TEST_USER = "TestUser"
TEST_PASS = "SecurePass123"

def delete_user(username):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username = %s", (username,))
    conn.commit()
    cur.close()
    conn.close()

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

def test_dashboard_redirect(driver_wait):
    driver, wait = driver_wait
    url_after = dashboard(driver)
    assert "/login" in url_after or "Login" in driver.page_source
