from requests_oauthlib import OAuth1Session
from colorama import Fore, Style


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
    print(f"{Fore.GREEN}[+] Preparing tweet payload...{Style.RESET_ALL}")
    payload = {"text": tweet_text}
    print(f"{Fore.BLUE}[*] Initializing OAuth session...{Style.RESET_ALL}")
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    print(f"{Fore.BLUE}[*] Posting tweet to Twitter API...{Style.RESET_ALL}")
    response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
    if response.status_code != 201:
        print(f"{Fore.RED}[!] Error occurred while posting tweet!{Style.RESET_ALL}")
        raise Exception(
            f"Request returned an error: {response.status_code} {response.text}")
    print(f"{Fore.GREEN}[+] Tweet posted successfully!{Style.RESET_ALL}")
    return response.json()