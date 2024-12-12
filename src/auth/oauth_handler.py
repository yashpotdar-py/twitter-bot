import time
import random
from utils.helper import get_env_var
from requests_oauthlib import OAuth1Session
from utils.selenium_setup import setup_selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TWITTER_USERNAME = get_env_var("TWITTER_USERNAME")
TWITTER_PASSWORD = get_env_var("TWITTER_PASSWORD")
TWITTER_EMAIL = get_env_var("TWITTER_EMAIL")
CONSUMER_KEY = get_env_var("CONSUMER_KEY")
CONSUMER_SECRET = get_env_var("CONSUMER_SECRET")


def get_twitter_verifier(auth_url):
    driver = setup_selenium(headless=False)

    try:
        driver.get(auth_url)
        time.sleep(random.uniform(1, 5))

        sign_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, "input[value='Sign In']"
            ))
        )
        sign_in_button.click()
        time.sleep(random.uniform(1, 5))

        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='text']"))
        )
        username_input.send_keys(TWITTER_USERNAME)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Next']/ancestor::button"))
        ).click()
        time.sleep(random.uniform(1, 5))

        if "unusual login activity" in driver.page_source.lower():
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, "input[name='text']")
                )).send_keys(TWITTER_EMAIL + Keys.RETURN)
        time.sleep(random.uniform(1, 5))

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='password']"))
        )
        password_input.send_keys(TWITTER_PASSWORD)
        time.sleep(random.uniform(1, 5))

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 "button[data-testid='LoginForm_Login_Button']")
            )
        ).click()
        time.sleep(random.uniform(1, 5))

        authorize_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input#allow"))
        )
        authorize_button.click()
        time.sleep(random.uniform(1, 5))

        verifier_code = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//code"))
        ).text
        return verifier_code
    except Exception as e:
        print(f"Error getting Twitter verifier code: {e}")
        return None

    finally:
        driver.quit()


def fetch_access_token():
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET)

    fetch_response = oauth.fetch_request_token(request_token_url)
    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")

    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    authorization_url = oauth.authorization_url(base_authorization_url)

    verifier = get_twitter_verifier(authorization_url)
    if not verifier:
        raise ValueError("Failed to retrieve verifier code.")

    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier,
    )

    oauth_tokens = oauth.fetch_access_token(access_token_url)
    return oauth_tokens["oauth_token"], oauth_tokens["oauth_token_secret"]
