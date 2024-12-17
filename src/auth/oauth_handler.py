"""
OAuth Handler Module

This module handles OAuth authentication for Twitter API access. It provides functionality
to authenticate users through Twitter's OAuth flow and obtain access tokens for API usage.

The module uses Selenium for automated browser interaction during the authentication process
and the requests_oauthlib library for OAuth token management.

Dependencies:
    - selenium
    - requests_oauthlib
    - colorama

Environment Variables Required:
    - TWITTER_USERNAME: Twitter account username
    - TWITTER_PASSWORD: Twitter account password
    - TWITTER_EMAIL: Twitter account email
    - CONSUMER_KEY: Twitter API consumer key
    - CONSUMER_SECRET: Twitter API consumer secret
"""

import time
import random
from src.utils.helper import get_env_var
from requests_oauthlib import OAuth1Session
from src.utils.selenium_setup import setup_selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import init, Fore, Style

init()  # Initialize colorama

TWITTER_USERNAME = get_env_var("TWITTER_USERNAME")
TWITTER_PASSWORD = get_env_var("TWITTER_PASSWORD")
TWITTER_EMAIL = get_env_var("TWITTER_EMAIL")
CONSUMER_KEY = get_env_var("CONSUMER_KEY")
CONSUMER_SECRET = get_env_var("CONSUMER_SECRET")


def get_twitter_verifier(auth_url, headless=True):
    """
    Automates the Twitter OAuth verification process using Selenium.

    This function navigates through Twitter's OAuth authorization flow by:
    1. Opening the authorization URL
    2. Logging in with provided credentials
    3. Handling any unusual login activity checks
    4. Authorizing the application
    5. Retrieving the verification code

    Args:
        auth_url (str): The Twitter OAuth authorization URL

    Returns:
        str: The OAuth verifier code if successful, None otherwise

    Raises:
        Exception: If any step in the verification process fails
    """
    print(f"{Fore.CYAN}[*] Starting Twitter verification process...{Style.RESET_ALL}")
    driver = setup_selenium(headless=headless)

    try:
        driver.get(auth_url)
        print(f"{Fore.CYAN}[*] Navigated to authorization URL{Style.RESET_ALL}")
        time.sleep(random.uniform(1, 5))

        sign_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, "input[value='Sign In']"
            ))
        )
        print(f"{Fore.BLUE}[+] Found Sign In button, clicking...{Style.RESET_ALL}")
        time.sleep(random.uniform(1, 5))
        sign_in_button.click()
        time.sleep(random.uniform(1, 5))

        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='text']"))
        )
        print(f"{Fore.GREEN}[+] Entering username data{Style.RESET_ALL}")
        time.sleep(random.uniform(1, 5))
        username_input.send_keys(TWITTER_USERNAME)
        time.sleep(random.uniform(1, 5))

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Next']/ancestor::button"))
        ).click()
        print(f"{Fore.BLUE}[+] Clicking Next button{Style.RESET_ALL}")
        time.sleep(random.uniform(1, 5))

        if "unusual login activity" in driver.page_source.lower():
            print(
                f"{Fore.YELLOW}[!] Detected unusual login activity{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[+] Entering email verification{Style.RESET_ALL}")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, "input[name='text']")
                )).send_keys(TWITTER_EMAIL + Keys.RETURN)

        time.sleep(random.uniform(1, 5))

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='password']"))
        )
        print(f"{Fore.GREEN}[+] Entering password data{Style.RESET_ALL}")
        time.sleep(random.uniform(1, 5))
        password_input.send_keys(TWITTER_PASSWORD)
        time.sleep(random.uniform(1, 5))

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 "button[data-testid='LoginForm_Login_Button']")
            )
        ).click()
        print(f"{Fore.BLUE}[+] Clicking Login button{Style.RESET_ALL}")
        time.sleep(random.uniform(1, 5))

        authorize_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input#allow"))
        )
        print(f"{Fore.BLUE}[+] Clicking Authorize button{Style.RESET_ALL}")
        authorize_button.click()
        time.sleep(random.uniform(1, 5))

        verifier_code = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//code"))
        ).text
        print(f"{Fore.CYAN}[*] Successfully retrieved verifier code{Style.RESET_ALL}")
        return verifier_code
    except Exception as e:
        print(f"{Fore.RED}[!] Error getting Twitter verifier code: {e}{Style.RESET_ALL}")
        return None

    finally:
        print(f"{Fore.CYAN}[*] Closing browser session{Style.RESET_ALL}")
        driver.quit()


def fetch_access_token(headless=True):
    """
    Performs the complete OAuth flow to obtain Twitter API access tokens.

    This function:
    1. Obtains a request token from Twitter
    2. Generates an authorization URL
    3. Gets the verifier code through browser automation
    4. Exchanges the verifier for access tokens

    Returns:
        tuple: A pair of (oauth_token, oauth_token_secret)

    Raises:
        ValueError: If the verifier code cannot be obtained
    """
    print(f"{Fore.CYAN}[*] Starting access token fetch process{Style.RESET_ALL}")
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET)

    fetch_response = oauth.fetch_request_token(request_token_url)
    print(f"{Fore.CYAN}[*] Successfully fetched request token{Style.RESET_ALL}")
    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")

    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    print(f"{Fore.CYAN}[*] Generated authorization URL{Style.RESET_ALL}")

    verifier = get_twitter_verifier(authorization_url, headless=headless)
    if not verifier:
        print(f"{Fore.RED}[!] Failed to retrieve verifier code{Style.RESET_ALL}")
        raise ValueError("Failed to retrieve verifier code.")

    print(f"{Fore.CYAN}[*] Exchanging verifier for access token{Style.RESET_ALL}")
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )

    oauth_tokens = oauth.fetch_access_token(access_token_url)
    print(f"{Fore.CYAN}[*] Successfully obtained access tokens{Style.RESET_ALL}")
    return oauth_tokens["oauth_token"], oauth_tokens["oauth_token_secret"]