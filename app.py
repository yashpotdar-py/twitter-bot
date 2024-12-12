from src.utils.helper import get_env_var
from src.twitter.post_tweet import post_tweet
from src.auth.oauth_handler import fetch_access_token

def main():
    try:
        access_token, access_token_secret = fetch_access_token()

        consumer_key = get_env_var("CONSUMER_KEY")
        consumer_secret = get_env_var("CONSUMER_SECRET")

        tweet_text = "Hello World! Pixel_Pancake69 here"

        response = post_tweet(
            access_token,
            access_token_secret,
            consumer_key,
            consumer_secret,
            tweet_text
        )
        print(response)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
