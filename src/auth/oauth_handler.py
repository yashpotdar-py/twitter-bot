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
import os
import sys
import time
import random
from src.bot_logger.logger import Logger
from src.utils.helper import get_env_var
from requests_oauthlib import OAuth1Session
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from src.utils.selenium_setup import setup_selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

project_root = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)


logger = Logger(__name__)
logger.info("Initializing OAuth Handler module")

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
    logger.info(
        "Initiating Twitter OAuth verification process")
    driver = setup_selenium(headless=headless)

    try:
        driver.get(auth_url)
        logger.info(
            "Successfully navigated to the authorization URL")
        time.sleep(random.uniform(1, 5))

        sign_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, "input[value='Sign In']"
            ))
        )
        logger.info(
            "Located Sign In button - proceeding with authentication")
        time.sleep(random.uniform(1, 5))
        sign_in_button.click()
        time.sleep(random.uniform(1, 5))

        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='text']"))
        )
        logger.info("Proceeding with username input")
        time.sleep(random.uniform(1, 5))
        username_input.send_keys(TWITTER_USERNAME)
        time.sleep(random.uniform(1, 5))

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Next']/ancestor::button"))
        ).click()
        logger.info("Proceeding to next authentication step")
        time.sleep(random.uniform(1, 5))

        if "unusual login activity" in driver.page_source.lower():
            logger.warning(
                "Security alert: Unusual login activity detected")
            logger.info(
                "Initiating email verification process")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, "input[name='text']")
                )).send_keys(TWITTER_EMAIL + Keys.RETURN)

        time.sleep(random.uniform(1, 5))

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='password']"))
        )
        logger.info("Proceeding with password authentication")
        time.sleep(random.uniform(1, 5))
        password_input.send_keys(TWITTER_PASSWORD)
        time.sleep(random.uniform(1, 5))

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 "button[data-testid='LoginForm_Login_Button']")
            )
        ).click()
        logger.info("Submitting login credentials")
        time.sleep(random.uniform(1, 5))

        authorize_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input#allow"))
        )
        logger.info("Proceeding with application authorization")
        authorize_button.click()
        time.sleep(random.uniform(1, 5))

        verifier_code = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//code"))
        ).text
        logger.success(
            "OAuth verifier code successfully retrieved")
        return verifier_code
    except Exception as e:
        logger.critical(
            f"Critical error encountered during verification process: {e}")
        return None

    finally:
        logger.info("Terminating browser session")
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
    logger.info(
        "Initiating OAuth access token acquisition process")
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET)

    fetch_response = oauth.fetch_request_token(request_token_url)
    logger.success(
        "Request token successfully acquired")
    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")

    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)
    logger.info("Authorization URL successfully generated")

    verifier = get_twitter_verifier(authorization_url, headless=headless)
    if not verifier:
        logger.critical(
            "OAuth verification process failed: Unable to obtain verifier code")
        raise ValueError(
            "OAuth verification process failed: Unable to obtain verifier code")

    logger.info(
        "Initiating verifier code exchange for access token")
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )

    oauth_tokens = oauth.fetch_access_token(access_token_url)
    logger.success(
        "Access tokens successfully acquired")
    return oauth_tokens["oauth_token"], oauth_tokens["oauth_token_secret"]
