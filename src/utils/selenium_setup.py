from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def setup_selenium(headless=True):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(
            '--disable-blink-features=AutomationControlled')
        if headless:
            chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=chrome_options)

        return driver
    except Exception as e:
        print(f"Error setting up Selenium: {e}")
        return None
