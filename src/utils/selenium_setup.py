from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

options = Options()
ua = UserAgent()
user_agent = ua.random


def setup_selenium(headless=True):
    try:
        chrome_options = Options()
        chrome_options.add_argument(
            '--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--start-maximized")
        options.add_argument(f'--user-agent={user_agent}')
        if headless:
            chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=chrome_options)

        # stealth(
        #     driver,
        #     user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        #     languages=["en-US", "en"],
        #     vendor="Google Inc.",
        #     platform="Win32",
        #     webgl_vendor="Intel Inc.",
        #     renderer="Intel Iris OpenGL Engine",
        #     fix_hairline=True,
        # )

        return driver
    except Exception as e:
        print(f"Error setting up Selenium: {e}")
        return None
