import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Paths
BASE_URL = "http://127.0.0.1:5000"

# ✅ Setup driver for CI with headless
def init_driver():
    options = Options()
    options.add_argument("--headless=new")  # headless for CI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    return driver, wait

# Login
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

# Register
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
    if "Fields cannot be empty!" in page_source or "Username already exists!" in page_source:
        return False
    return "Registration successful!" in page_source

# Dashboard
def dashboard(driver):
    driver.get(BASE_URL + "/dashboard")
    return driver.current_url

# Logout
def logout(driver, wait):
    driver.get(BASE_URL + "/dashboard")
    l_button = wait.until(EC.element_to_be_clickable((By.NAME, "logout")))
    l_button.click()
