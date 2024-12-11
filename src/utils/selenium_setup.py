# src\utils\selenium_setup.py
"""
Sets up a Selenium Chrome driver with the specified options.

Args:
    headless (bool): If True, the Chrome browser will run in headless mode (without a GUI).

Returns:
    webdriver.Chrome: A Selenium Chrome driver instance with the specified options.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver(headless=True):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    if headless:
        chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    return driver