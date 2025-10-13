import os
import time
import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

<<<<<<< HEAD
# Base URL for Flask app
BASE_URL = "http://127.0.0.1:5000"

# --- Database Config ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/flask_db")


# ✅ Initialize table in PostgreSQL (for CI)
def init_test_db():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


# ✅ Delete test user if exists (cleanup before each test)
def delete_user(username):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE username = %s;", (username,))
    conn.commit()
    cur.close()
    conn.close()


# ✅ Headless Chrome setup for GitHub Actions
def init_driver():
    options = Options()
    options.add_argument("--headless=new")
=======
BASE_URL = "http://127.0.0.1:5000"

def init_driver():
    """Initialize Chrome WebDriver"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # For CI environments
>>>>>>> 0814dd0b79ecc69e8473dcb22afe612d3371f668
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    return driver, wait

<<<<<<< HEAD

# ✅ Register function
def register(driver, wait, username_val, password_val):
    driver.get(BASE_URL + "/register")
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username_val)
    wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password_val)
=======
def register(driver, wait, username, password):
    driver.get(BASE_URL + "/register")
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
    wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)
>>>>>>> 0814dd0b79ecc69e8473dcb22afe612d3371f668
    wait.until(EC.element_to_be_clickable((By.NAME, "register"))).click()
    time.sleep(1)
    return "Registration successful!" in driver.page_source

<<<<<<< HEAD
    html = driver.page_source
    if "Fields cannot be empty!" in html or "Username already exists!" in html:
        return False
    return "Registration successful!" in html


# ✅ Login function
def login(driver, wait, username_val, password_val):
    driver.get(BASE_URL + "/login")
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username_val)
    wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password_val)
    wait.until(EC.element_to_be_clickable((By.NAME, "login"))).click()
    time.sleep(1)

    html = driver.page_source
    if "Invalid username or password!" in html or "Please log in first!" in html:
        return False
    return "Dashboard" in html or "Welcome" in html


# ✅ Dashboard direct access test
=======
def login(driver, wait, username, password):
    driver.get(BASE_URL + "/login")
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
    wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.NAME, "login"))).click()
    time.sleep(1)
    return "Dashboard" in driver.page_source

>>>>>>> 0814dd0b79ecc69e8473dcb22afe612d3371f668
def dashboard(driver):
    driver.get(BASE_URL + "/dashboard")
    return driver.current_url

<<<<<<< HEAD

# ✅ Logout function
def logout(driver, wait):
    driver.get(BASE_URL + "/dashboard")
    try:
        wait.until(EC.element_to_be_clickable((By.NAME, "logout"))).click()
    except:
        pass
    time.sleep(1)
=======
def logout(driver):
    driver.get(BASE_URL + "/logout")
    time.sleep(1)
    return "Login" in driver.page_source
>>>>>>> 0814dd0b79ecc69e8473dcb22afe612d3371f668
