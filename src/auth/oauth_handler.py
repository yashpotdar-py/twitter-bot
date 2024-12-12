"""
Provides functions to obtain OAuth 1.0a tokens and authorization URLs for Twitter API access.

The `get_oauth_token` function retrieves the initial request token and secret needed to authorize an application to access the Twitter API on behalf of a user.

The `get_authorization_url` function generates the authorization URL that the user must visit to grant the application access to their account. This URL is constructed using the request token and secret obtained from `get_oauth_token`.
"""
# src\auth\oauth_handler.py

from requests_oauthlib import OAuth1Session

def get_oauth_token(consumer_key, consumer_secret):
    request_token_url = 'https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write'
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    return oauth.fetch_request_token(request_token_url)

def get_authorization_url(tokens):
    base_authorization_url = 'https://api.twitter.com/oauth/authorize'
    oauth = OAuth1Session(
        client_key=tokens['oauth_token'],
        client_secret=tokens['oauth_token_secret']
    )
    return oauth.authorization_url(base_authorization_url)

