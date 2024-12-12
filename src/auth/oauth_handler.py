import logging
from requests_oauthlib import OAuth1Session

"""
OAuth Handler Module

This module provides functionality for handling OAuth authentication with the Twitter API.
It includes methods for obtaining request tokens, generating authorization URLs, and
retrieving access tokens.

The module uses the requests_oauthlib library for OAuth1 authentication and implements
logging to track authentication processes.

Dependencies:
    - requests_oauthlib
    - logging

Note:
    All OAuth-related errors are logged and re-raised for proper error handling
    in the calling code.
"""

# Set up logging for authentication processes
auth_logger = logging.getLogger("auth")
auth_logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/auth.log")
handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
auth_logger.addHandler(handler)


def get_oauth_tokens(consumer_key, consumer_secret):
    """
    Retrieve OAuth tokens for the application.

    This function initiates the OAuth flow by obtaining request tokens from Twitter's API.
    It creates an OAuth1Session using the provided consumer credentials and makes a
    request to Twitter's request token endpoint.

    Args:
        consumer_key (str): The consumer key for the Twitter API.
        consumer_secret (str): The consumer secret for the Twitter API.

    Returns:
        dict: A dictionary containing the request token and secret with keys:
            - oauth_token: The request token
            - oauth_token_secret: The request token secret

    Raises:
        Exception: If there is any error in fetching the request tokens from Twitter API.

    Example:
        tokens = get_oauth_tokens("your_consumer_key", "your_consumer_secret")
    """
    auth_logger.info("Fetching OAuth request tokens.")
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

    try:
        fetch_response = oauth.fetch_request_token(request_token_url)
        auth_logger.info("OAuth request tokens retrieved successfully.")
        return {
            "oauth_token": fetch_response.get("oauth_token"),
            "oauth_token_secret": fetch_response.get("oauth_token_secret"),
        }
    except Exception as e:
        auth_logger.error(f"Error fetching OAuth request tokens: {e}")
        raise


def get_authorization_url(tokens):
    """
    Generate the authorization URL for the user to approve the app.

    This function creates an authorization URL that the user needs to visit to authorize
    the application. It uses the request tokens obtained from get_oauth_tokens() along
    with the consumer credentials.

    Args:
        tokens (dict): A dictionary containing the following keys:
            - consumer_key: The application's consumer key
            - consumer_secret: The application's consumer secret
            - oauth_token: The request token obtained from get_oauth_tokens
            - oauth_token_secret: The request token secret obtained from get_oauth_tokens

    Returns:
        str: The authorization URL that the user should visit to authorize the application.

    Raises:
        Exception: If there is any error in generating the authorization URL.

    Example:
        auth_url = get_authorization_url({
            "consumer_key": "your_key",
            "consumer_secret": "your_secret",
            "oauth_token": "request_token",
            "oauth_token_secret": "request_token_secret"
        })
    """
    auth_logger.info("Generating authorization URL.")
    base_authorization_url = "https://api.twitter.com/oauth/authorize"
    oauth = OAuth1Session(
        client_key=tokens.get("consumer_key"),
        client_secret=tokens.get("consumer_secret"),
        resource_owner_key=tokens.get("oauth_token"),
        resource_owner_secret=tokens.get("oauth_token_secret"),
    )

    try:
        authorization_url = oauth.authorization_url(base_authorization_url)
        auth_logger.info(f"Authorization URL generated: {authorization_url}")
        return authorization_url
    except Exception as e:
        auth_logger.error(f"Error generating authorization URL: {e}")
        raise


def get_access_tokens(consumer_key, consumer_secret, oauth_token, oauth_token_secret, verifier):
    """
    Retrieve access tokens using the verifier code.

    This function completes the OAuth flow by exchanging the request tokens and verifier
    code for access tokens. These access tokens can be used for making authenticated
    requests to the Twitter API.

    Args:
        consumer_key (str): The consumer key for the Twitter API.
        consumer_secret (str): The consumer secret for the Twitter API.
        oauth_token (str): The request token obtained from get_oauth_tokens.
        oauth_token_secret (str): The request token secret obtained from get_oauth_tokens.
        verifier (str): The verifier code provided by Twitter after user authorization.

    Returns:
        dict: A dictionary containing the access tokens with keys:
            - access_token: The OAuth access token
            - access_token_secret: The OAuth access token secret

    Raises:
        Exception: If there is any error in fetching the access tokens from Twitter API.

    Example:
        access_tokens = get_access_tokens(
            "consumer_key",
            "consumer_secret",
            "oauth_token",
            "oauth_token_secret",
            "verifier_code"
        )
    """
    auth_logger.info("Fetching access tokens using verifier code.")
    access_token_url = "https://api.twitter.com/oauth/access_token"
    oauth = OAuth1Session(
        client_key=consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=oauth_token,
        resource_owner_secret=oauth_token_secret,
        verifier=verifier,
    )

    try:
        oauth_tokens = oauth.fetch_access_token(access_token_url)
        auth_logger.info("Access tokens retrieved successfully.")
        return {
            "access_token": oauth_tokens.get("oauth_token"),
            "access_token_secret": oauth_tokens.get("oauth_token_secret"),
        }
    except Exception as e:
        auth_logger.error(f"Error fetching access tokens: {e}")
        raise
