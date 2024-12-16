from src.utils.helper import get_env_var
from src.twitter.post_tweet import post_tweet
from src.auth.oauth_handler import fetch_access_token
from src.ai.tweet_generator import TweetGenerator


def main():
    try:
        access_token, access_token_secret = fetch_access_token()

        consumer_key = get_env_var("CONSUMER_KEY")
        consumer_secret = get_env_var("CONSUMER_SECRET")

        tweet_generator = TweetGenerator()
        tweet_text = tweet_generator.generate_tweet(
            phase="phase_2", topic="action adventure")

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
