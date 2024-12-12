from requests_oauthlib import OAuth1Session


def post_tweet(access_token, access_token_secret, consumer_key, consumer_secret, tweet_text):
    payload = {"text": tweet_text}
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
    if response.status_code != 201:
        raise Exception(
            f"Request returned an error: {response.status_code} {response.text}")
    return response.json()
