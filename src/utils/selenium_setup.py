from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from colorama import Fore, Style, init

init()  # Initialize colorama

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
        print(f"{Fore.CYAN}[*] Initializing Chrome options...{Style.RESET_ALL}")
        chrome_options = Options()
        chrome_options.add_argument(
            '--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--start-maximized")
        options.add_argument(f'--user-agent={user_agent}')
        if headless:
            print(f"{Fore.YELLOW}[*] Running in headless mode{Style.RESET_ALL}")
            chrome_options.add_argument("--headless")
        print(f"{Fore.GREEN}[*] Setting up Chrome driver...{Style.RESET_ALL}")
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=chrome_options)
        print(f"{Fore.BLUE}[+] Selenium setup completed successfully{Style.RESET_ALL}")
        return driver
    except Exception as e:
        print(f"{Fore.RED}[!] Error setting up Selenium: {e}{Style.RESET_ALL}")
        return None