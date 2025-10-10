import os
import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Paths
CHROME_PATH = r"C:\chromedriver-win64\chromedriver.exe"
BASE_URL = "http://127.0.0.1:5000"
DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

# -----------------------------
# DATABASE FUNCTIONS
# -----------------------------
def init_test_db():
    """Initialize SQLite test DB schema if missing."""
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

def delete_user(username):
    """Delete a user from DB if exists."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()

# -----------------------------
# SELENIUM DRIVER
# -----------------------------
def init_driver():
    """Initialize Chrome WebDriver for local or GitHub Actions."""
    options = Options()
    
    # Run headless in CI
    if os.name != "nt":
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.binary_location = "/usr/bin/chromium-browser"

    if os.name == "nt":
        service = Service(CHROME_PATH)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)

    wait = WebDriverWait(driver, 10)
    return driver, wait

# -----------------------------
# APP INTERACTION
# -----------------------------
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
    time.sleep(1)

    page_source = driver.page_source
    if "Invalid username or password!" in page_source or "Please log in first!" in page_source:
        return False

    try:
        logout_btn = wait.until(EC.element_to_be_clickable((By.NAME, "logout")))
        logout_btn.click()
    except:
        pass

    return True

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
    if "Fields cannot be empty!" in page_source:
        return False
    if "Username too long!" in page_source:
        return False
    if "Password too long!" in page_source:
        return False
    if "Username already exists!" in page_source:
        return False

    return "Registration successful!" in page_source

def dashboard(driver):
    driver.get(BASE_URL + "/dashboard")
    return driver.current_url

def logout(driver, wait):
    driver.get(BASE_URL + "/dashboard")
    try:
        l_button = wait.until(EC.element_to_be_clickable((By.NAME, "logout")))
        l_button.click()
    except:
        pass
