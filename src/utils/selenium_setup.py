import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

"""
This module provides functionality for setting up and configuring Selenium WebDriver
for automated web browser testing and interaction.

The module includes:
- Logging configuration for Selenium operations
- WebDriver setup with customizable options
- Chrome-specific configuration and automation controls
"""

# Set up logging for Selenium
selenium_logger = logging.getLogger("selenium_setup")
selenium_logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/app.log")
handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
selenium_logger.addHandler(handler)


def setup_selenium_driver(headless=True):
    """
    Set up and configure the Selenium WebDriver with Chrome browser.

    This function initializes a Chrome WebDriver instance with specific configurations
    for automated testing. It includes options to disable GPU, sandbox, and automation
    detection, as well as the ability to run in headless mode.

    Args:
        headless (bool): Whether to run Chrome in headless mode. Defaults to True.

    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance.

    Raises:
        Exception: If there's an error during WebDriver setup, the error is logged
                  and re-raised.

    Example:
        driver = setup_selenium_driver(headless=True)
        driver.get("https://example.com")
        driver.quit()
    """
    selenium_logger.info("Setting up Selenium WebDriver.")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        if headless:
            # Run in headless mode for automation
            chrome_options.add_argument("--headless")
        chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        selenium_logger.info("Selenium WebDriver setup successful.")
        return driver
    except Exception as e:
        selenium_logger.error(f"Error setting up Selenium WebDriver: {e}")
        raise
