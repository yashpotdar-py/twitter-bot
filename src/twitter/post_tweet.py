"""
Posts a tweet to the Twitter API using the provided OAuth credentials.

Args:
    consumer_key (str): The consumer key for the Twitter API.
    consumer_secret (str): The consumer secret for the Twitter API.
    access_token (str): The access token for the Twitter API.
    access_token_secret (str): The access token secret for the Twitter API.
    tweet_text (str): The text of the tweet to be posted.

Raises:
    Exception: If the Twitter API request returns an error status code.
"""
# src\twitter\post_tweet.py

from requests_oauthlib import OAuth1Session

def post_tweet(consumer_key, consumer_secret, access_token, access_token_secret, tweet_text):
    payload = {
        "text": tweet_text
    }

    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret
    )
    response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )