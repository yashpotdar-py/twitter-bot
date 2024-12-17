"""
This script handles the main workflow for generating and posting tweets.
It performs the following steps:
1. Fetches access tokens for Twitter API authentication
2. Gets environment variables for API credentials
3. Initializes the tweet generator
4. Generates tweet content based on specified phase and topic
5. Posts the generated tweet to Twitter
"""

from src.utils.helper import get_env_var
from src.twitter.post_tweet import post_tweet
from src.auth.oauth_handler import fetch_access_token
from src.ai.tweet_generator import TweetGenerator
from colorama import Fore, Style


def main(debug=False):
    """
    Main function that orchestrates the tweet generation and posting process.
    Handles authentication, content generation, and Twitter API interaction.

    Raises:
        Exception: Any error that occurs during the process will be caught and displayed
    """
    try:
        print(f"{Fore.CYAN}[*] Fetching access tokens...{Style.RESET_ALL}")
        headless = not debug
        access_token, access_token_secret = fetch_access_token(
            headless=headless)
        print(f"{Fore.GREEN}[+] Getting environment variables...{Style.RESET_ALL}")
        consumer_key = get_env_var("CONSUMER_KEY")
        consumer_secret = get_env_var("CONSUMER_SECRET")

        print(f"{Fore.YELLOW}[*] Initializing tweet generator...{Style.RESET_ALL}")
        tweet_generator = TweetGenerator()
        print(f"{Fore.MAGENTA}[*] Generating tweet content...{Style.RESET_ALL}")
        tweet_text = tweet_generator.generate_tweet(
            phase="phase_2", topic="action adventure")

        print(f"{Fore.BLUE}[*] Posting tweet to Twitter...{Style.RESET_ALL}")
        response = post_tweet(
            access_token,
            access_token_secret,
            consumer_key,
            consumer_secret,
            tweet_text
        )
        print(f"{Fore.GREEN}[+] Response received: {response}{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode')
    args = parser.parse_args()
    main(debug=args.debug)