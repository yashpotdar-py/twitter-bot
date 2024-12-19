import os
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from fake_useragent import UserAgent
from src.bot_logger.logger import Logger
from webdriver_manager.chrome import ChromeDriverManager

project_root = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)


logger = Logger(__name__)
logger.info("Initiating Selenium WebDriver setup process...")

options = Options()
ua = UserAgent()
user_agent = ua.random


def setup_selenium(headless=True):
    """
    Sets up and configures a Chrome WebDriver instance with custom options for web automation.

    Args:
        headless (bool): If True, runs Chrome in headless mode without GUI. Defaults to True.

    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance if successful, None if setup fails.

    Features:
        - Disables automation detection
        - Maximizes browser window
        - Uses random user agent
        - Optional headless mode
        - Automatic ChromeDriver installation
    """
    try:
        logger.info(
            "Initializing Chrome WebDriver configuration parameters...")
        chrome_options = Options()
        chrome_options.add_argument(
            '--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--start-maximized")
        options.add_argument(f'--user-agent={user_agent}')
        if headless:
            logger.info(
                "Enabling headless mode for Chrome WebDriver")
            chrome_options.add_argument("--headless")
        logger.info("Proceeding with Chrome WebDriver initialization...")
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=chrome_options)
        logger.success(
            "Chrome WebDriver initialization completed successfully")
        return driver
    except Exception as e:
        logger.critical(
            f"Critical error encountered during WebDriver initialization: {e}")
        return None
