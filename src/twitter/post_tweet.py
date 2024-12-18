import os
import sys
from src.bot_logger.logger import Logger
from requests_oauthlib import OAuth1Session

project_root = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)


logger = Logger(__name__)
logger.info("Initializing Twitter Post Tweet Module")


def post_tweet(access_token, access_token_secret, consumer_key, consumer_secret, tweet_text):
    """
    Posts a tweet to Twitter using the Twitter API v2.

    Args:
        access_token (str): The OAuth access token for authentication
        access_token_secret (str): The OAuth access token secret for authentication
        consumer_key (str): The Twitter API consumer key
        consumer_secret (str): The Twitter API consumer secret
        tweet_text (str): The text content of the tweet to be posted

    Returns:
        dict: The JSON response from the Twitter API containing the posted tweet data

    Raises:
        Exception: If the API request fails or returns an error status code
    """
    logger.info("Initiating tweet payload preparation")
    payload = {"text": tweet_text}
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    logger.info("Initiating API request to Twitter endpoint")
    response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
    if response.status_code != 201:
        logger.error(
            "Request failed: Unable to post tweet to Twitter API")
        raise Exception(
            f"Request returned an error: {response.status_code} {response.text}")
    logger.success("Tweet successfully published to Twitter platform")
    return response.json()
