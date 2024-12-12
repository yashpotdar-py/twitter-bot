import logging
from requests_oauthlib import OAuth1Session

"""
Twitter API Integration Module

This module provides functionality to post tweets using Twitter API v2.
It includes logging capabilities to track API interactions and error handling.

Dependencies:
    - requests_oauthlib: For OAuth1 authentication with Twitter API
    - logging: For logging API interactions and errors

The module sets up a dedicated logger for Twitter-related actions that writes to 'logs/twitter.log'.
"""

# Set up logging for Twitter-related actions
twitter_logger = logging.getLogger("twitter")
twitter_logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/twitter.log")
handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
twitter_logger.addHandler(handler)


def post_tweet(consumer_key, consumer_secret, access_token, access_token_secret, tweet_text):
    """
    Post a tweet using Twitter API v2.

    This function authenticates with the Twitter API using OAuth1 and posts a tweet
    with the provided text. It includes error handling and logging of the API interaction.

    Args:
        consumer_key (str): The consumer key for the Twitter API authentication.
        consumer_secret (str): The consumer secret for the Twitter API authentication.
        access_token (str): The access token for the Twitter API authorization.
        access_token_secret (str): The access token secret for the Twitter API authorization.
        tweet_text (str): The text content of the tweet to post.

    Returns:
        dict: The JSON response from the Twitter API containing the posted tweet details.

    Raises:
        requests.exceptions.HTTPError: If the Twitter API returns a non-201 status code.
        Exception: For any other errors that occur during the API interaction.

    Example:
        >>> response = post_tweet(
        ...     "consumer_key",
        ...     "consumer_secret",
        ...     "access_token",
        ...     "access_token_secret",
        ...     "Hello, Twitter!"
        ... )
        >>> print(response)
    """
    twitter_logger.info("Preparing to post a tweet.")
    url = "https://api.twitter.com/2/tweets"
    payload = {"text": tweet_text}

    oauth = OAuth1Session(
        client_key=consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    try:
        twitter_logger.info("Sending request to Twitter API.")
        response = oauth.post(url, json=payload)

        if response.status_code != 201:
            twitter_logger.error(
                f"Error posting tweet: {response.status_code} {response.text}")
            response.raise_for_status()

        twitter_logger.info("Tweet posted successfully.")
        return response.json()
    except Exception as e:
        twitter_logger.error(f"Failed to post tweet: {e}")
        raise
