import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Paths
CHROME_PATH = r"C:\chromedriver-win64\chromedriver.exe"
BASE_URL = "http://127.0.0.1:5000"
DB_PATH = r"C:\Personal\Testing\selenium-flask-auth\users.db"


# ✅ Ensure test DB schema exists
def init_test_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL CHECK(length(username) <= 30),
            password TEXT NOT NULL CHECK(length(password) <= 50)
        )
    """)
    conn.commit()
    conn.close()


# ✅ Utility to delete user (for clean test runs)
def delete_user(username):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()


# ✅ Setup driver
def init_driver():
    service = Service(CHROME_PATH)
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 10)
    return driver, wait


# ✅ Login function
def login(driver, wait, username_val, password_val):
    driver.get(BASE_URL + "/login")

    username = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    login_btn = wait.until(EC.element_to_be_clickable((By.NAME, "login")))

    username.clear()
    username.send_keys(username_val)
    password.clear()
    password.send_keys(password_val)
    login_btn.click()

    time.sleep(1)  # allow page to reload
    page_source = driver.page_source

    # ❌ Check for failed login first
    if "Invalid username or password!" in page_source:
        return False
    if "Please log in first!" in page_source:
        return False

    # ✅ Only attempt logout if login succeeded
    try:
        logout_btn = wait.until(EC.element_to_be_clickable((By.NAME, "logout")))
        logout_btn.click()
    except:
        pass

    return True



# ✅ Dashboard function
def dashboard(driver):
    driver.get(BASE_URL + "/dashboard")
    return driver.current_url 

# ✅ Register function
def register(driver, wait, username_val, password_val):
    driver.get(BASE_URL + "/register")

    r_username = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    r_password = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    r_button = wait.until(EC.element_to_be_clickable((By.NAME, "register")))

    r_username.clear()
    r_username.send_keys(username_val)
    r_password.clear()
    r_password.send_keys(password_val)
    r_button.click()

    time.sleep(1)
    page_source = driver.page_source

    # ✅ Match Flask flash messages
    if "Fields cannot be empty!" in page_source:
        return False
    if "Username too long!" in page_source:
        return False
    if "Password too long!" in page_source:
        return False
    if "Username already exists!" in page_source:
        return False

    return "Registration successful!" in page_source

def logout(driver, wait):
    driver.get(BASE_URL + "/dashboard")
    l_button = wait.until(EC.element_to_be_clickable((By.NAME, "logout")))
    l_button.click()
