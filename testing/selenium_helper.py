import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://127.0.0.1:5000"

def init_driver():
    """Initialize Chrome WebDriver"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # For CI environments
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    return driver, wait

def register(driver, wait, username, password):
    driver.get(BASE_URL + "/register")
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
    wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.NAME, "register"))).click()
    time.sleep(1)
    return "Registration successful!" in driver.page_source

def login(driver, wait, username, password):
    driver.get(BASE_URL + "/login")
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
    wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)
    wait.until(EC.element_to_be_clickable((By.NAME, "login"))).click()
    time.sleep(1)
    return "Dashboard" in driver.page_source

def dashboard(driver):
    driver.get(BASE_URL + "/dashboard")
    return driver.current_url

def logout(driver):
    driver.get(BASE_URL + "/logout")
    time.sleep(1)
    return "Login" in driver.page_source
