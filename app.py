"""
This script handles the main workflow for generating and posting tweets.
It performs the following steps:
1. Fetches access tokens for Twitter API authentication
2. Gets environment variables for API credentials
3. Initializes the tweet generator
4. Generates tweet content based on specified phase and topic
5. Posts the generated tweet to Twitter
"""
import os
import sys
import random
from src.utils.helper import get_env_var
from src.bot_logger.logger import Logger
from src.twitter.post_tweet import post_tweet
from src.auth.oauth_handler import fetch_access_token
from src.ai.tweet_generator import TweetGenerator

project_root = os.path.abspath(os.path.join(
    os.path.dirname(__file__)))
sys.path.insert(0, project_root)


logger = Logger("app")
logger.info("Starting tweet generation application")


def main(debug=False):
    """
    Main function that orchestrates the tweet generation and posting process.
    Handles authentication, content generation, and Twitter API interaction.

    Raises:
        Exception: Any error that occurs during the process will be caught and displayed
    """
    try:
        logger.info("Initiating OAuth authentication process for Twitter API")
        headless = not debug
        access_token, access_token_secret = fetch_access_token(
            headless=headless)
        logger.success("Successfully obtained OAuth access tokens")

        logger.info("Retrieving API credentials from environment variables")
        consumer_key = get_env_var("CONSUMER_KEY")
        consumer_secret = get_env_var("CONSUMER_SECRET")
        logger.success("API credentials successfully loaded")

        logger.info("Initializing AI-powered tweet generation system")
        tweet_generator = TweetGenerator()

        logger.info(
            "Beginning tweet content generation process for phase_2 with action adventure topic")
        topics = ["open-world RPG",
                  "sandbox game",
                  "action-adventure",
                  "story-driven narrative game",
                  "survival game",
                  "roguelike dungeon crawler",
                  "puzzle-platformer",
                  "simulation/management game",
                  "quirky indie game with a deep meaning",
                  "retro 8-bit adventure",
                  "cozy farming sim",
                  "time-loop mystery game",
                  "social deduction multiplayer",
                  "dark souls-like challenge",
                  "post-apocalyptic survival",
                  "whimsical cooking sim",
                  "narrative-driven walking simulator",
                  "satirical life sim",
                  "cyberpunk exploration game",
                  "space-travel sandbox",
                  "unexpectedly emotional visual novel",
                  "chaotic party game",
                  "episodic adventure series",
                  "absurd physics sandbox",
                  "comedic point-and-click adventure"
                  ]
        phases = ["phase_1", "phase_2", "phase_3", "phase_4", "phase_5"]
        tweet_topic = random.choice(topics)
        tweet_phase = random.choice(phases)
        tweet_text = tweet_generator.generate_tweet(
            phase=tweet_phase, topic=tweet_topic)
        logger.success("Tweet content successfully generated")

        logger.info("Initiating Twitter API request to post tweet")
        response = post_tweet(
            access_token,
            access_token_secret,
            consumer_key,
            consumer_secret,
            tweet_text
        )
        logger.success(f"Tweet successfully posted. API Response: {response}")
        logger.info(
            "Tweet generation and posting process completed successfully")

    except Exception as e:
        logger.error(
            f"Critical error encountered during tweet generation process: {str(e)}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode')
    args = parser.parse_args()
    main(debug=args.debug)
