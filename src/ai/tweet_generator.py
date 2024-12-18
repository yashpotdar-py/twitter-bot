"""
Tweet Generator Module

This module provides functionality for generating gaming-related tweets using Google's
Generative AI. It maintains personality consistency and avoids duplicate content through
similarity checking.

The TweetGenerator class handles:
- Loading and managing AI personality traits
- Tweet storage and retrieval
- Content similarity analysis
- Integration with Google's AI API
- Gaming topic categorization and examples

Key Features:
- Customizable tweet length limits
- Similarity threshold for duplicate detection
- Persistent storage of generated tweets
- Rich gaming category classification
- Color-coded console output

Dependencies:
- google.generativeai: For AI text generation
- sklearn: For text similarity analysis
- colorama: For console text formatting
- dotenv: For environment variable management

Example Usage:
    generator = TweetGenerator()
    tweet = generator.generate_tweet(topic="indie games")
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, List, Optional
from src.bot_logger.logger import Logger
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

project_root = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)


logger = Logger(__name__)
logger.info("Initializing Tweet Generator Module")


try:
    import google.generativeai as genai
except ImportError:
    logger.error(
        "ERROR: Required dependency 'google-generativeai' is not installed")
    logger.error("Please execute: pip install google-generativeai")
    raise

load_dotenv()


class TweetGenerator:
    def __init__(self,
                 personality_filepath: str = 'src/ai/personality.json',
                 tweet_storage_filepath: str = 'src/ai/tweets.json',
                 max_tweet_length: int = 280,
                 similarity_threshold: float = 0.9):
        logger.info(
            "Initiating TweetGenerator initialization sequence")
        self.personality = self.load_personality(personality_filepath)
        self.tweet_storage_filepath = tweet_storage_filepath
        self.max_tweet_length = max_tweet_length
        self.similarity_threshold = similarity_threshold
        self.configure_api()
        self.tweet_storage = self.load_tweet_storage()
        logger.success(
            "TweetGenerator initialization completed successfully")
        self.game_types = {
            "indie games": ["Stardew Valley", "Hollow Knight", "Undertale", "Hades", "Celeste"],
            "game development": ["Unity", "Unreal Engine", "Godot"],
            "gaming culture": ["Minecraft", "Fortnite", "Among Us", "The Legend of Zelda", "Dark Souls"],
            "open world": ["The Witcher 3", "Red Dead Redemption 2", "Breath of the Wild", "Skyrim", "Elden Ring"],
            "sandbox": ["Minecraft", "Terraria", "No Man's Sky", "Space Engineers", "Garry's Mod"],
            "action adventure": ["God of War", "Horizon Zero Dawn", "Spider-Man", "Tomb Raider", "Uncharted", "God of War: Ragnarok"],
            "narrative games": ["Life is Strange", "The Walking Dead", "Detroit: Become Human", "Firewatch", "What Remains of Edith Finch"],
            "survival": ["Valheim", "The Forest", "Subnautica", "Don't Starve", "Rust"],
            "roguelike": ["Hades", "Dead Cells", "Enter the Gungeon", "Risk of Rain 2", "Slay the Spire"],
            "puzzle platformer": ["Portal", "Braid", "Inside", "Limbo", "Fez"],
            "simulation": ["Rimworld", "Cities: Skylines", "Planet Coaster", "Two Point Hospital", "Factorio"],
            "retro": ["Shovel Knight", "Hyper Light Drifter", "CrossCode", "Axiom Verge", "Octopath Traveler"],
            "farming sim": ["Stardew Valley", "My Time at Portia", "Story of Seasons", "Farm Together", "Sun Haven"],
            "time loop": ["Outer Wilds", "Deathloop", "12 Minutes", "Loop Hero", "Minit"],
            "social deduction": ["Among Us", "Project Winter", "Town of Salem", "Secret Neighbor", "Goose Goose Duck"],
            "soulslike": ["Dark Souls", "Bloodborne", "Nioh", "Mortal Shell", "Salt and Sanctuary"],
            "post apocalyptic": ["Fallout", "Metro Exodus", "The Last of Us", "Days Gone", "Mad Max"],
            "cooking": ["Overcooked", "Cooking Simulator", "Chef Life", "Cooking Mama", "Battle Chef Brigade"],
            "walking sim": ["Gone Home", "Dear Esther", "The Stanley Parable", "Everybody's Gone to the Rapture", "The Vanishing of Ethan Carter"],
            "cyberpunk": ["Cyberpunk 2077", "Ghostrunner", "The Ascent", "Cloudpunk", "Observer"],
            "space sandbox": ["Kerbal Space Program", "Elite Dangerous", "Star Citizen", "Astroneer", "Space Engineers"],
            "visual novel": ["Doki Doki Literature Club", "VA-11 Hall-A", "Phoenix Wright", "Steins;Gate", "Zero Escape"],
            "party games": ["Jackbox Party Pack", "Fall Guys", "Ultimate Chicken Horse", "Moving Out", "Overcooked"],
            "episodic": ["Life is Strange", "The Wolf Among Us", "Tales from the Borderlands", "Kentucky Route Zero", "Batman: The Telltale Series"],
            "physics sandbox": ["Totally Accurate Battle Simulator", "Human: Fall Flat", "Gang Beasts", "Goat Simulator", "BeamNG.drive"],
            "point and click": ["Monkey Island", "Grim Fandango", "Day of the Tentacle", "Sam & Max", "Thimbleweed Park"]
        }

    def load_personality(self, filepath: str) -> Dict:
        logger.info(
            f"Initiating personality data load from: {filepath}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                personality = json.load(f)
                logger.success(
                    "Personality data loaded successfully")
                return personality
        except Exception as e:
            logger.error(
                f"ERROR: Personality data load operation failed: {e}")
            raise ValueError(
                f"ERROR: Personality data load operation failed: {e}")

    def load_tweet_storage(self) -> List[Dict]:
        logger.info("Initiating tweet storage load operation")
        if os.path.exists(self.tweet_storage_filepath):
            try:
                with open(self.tweet_storage_filepath, 'r', encoding='utf-8') as f:
                    tweets = json.load(f)
                    logger.info(
                        "Tweet storage loaded successfully")
                    return tweets
            except json.JSONDecodeError:
                logger.warning(
                    "WARNING: Tweet storage file is invalid or empty")
                return []
        logger.warning(
            "NOTICE: Tweet storage file not found. Initializing empty storage")
        return []

    def save_tweet_storage(self):
        logger.info("Initiating tweet storage save operation")
        with open(self.tweet_storage_filepath, 'w', encoding='utf-8') as f:
            json.dump(self.tweet_storage, f, indent=4)
        logger.success("Tweet storage save operation completed successfully")

    def is_similar_to_existing(self, new_tweet: str) -> bool:
        logger.info("Initiating tweet similarity analysis")
        existing_tweets = [tweet['text'] for tweet in self.tweet_storage]
        if not existing_tweets:
            logger.warning(
                "NOTICE: No existing tweets available for comparison")
            return False

        new_tweet_processed = ' '.join(word.lower()
                                       for word in new_tweet.split())
        existing_tweets_processed = [
            ' '.join(word.lower() for word in tweet.split()) for tweet in existing_tweets]

        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=1000
        ).fit_transform([new_tweet_processed] + existing_tweets_processed)

        cosine_similarities = cosine_similarity(
            vectorizer[0:1], vectorizer[1:]).flatten()

        max_similarity = max(cosine_similarities) if len(
            cosine_similarities) > 0 else 0

        is_similar = max_similarity >= self.similarity_threshold
        logger.info(
            f"Similarity analysis complete. Result: {is_similar}")
        return is_similar

    def configure_api(self):
        logger.info("Initiating API configuration")
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            logger.critical(
                "CRITICAL ERROR: API key not found in environment configuration")
            raise ValueError(
                "ERROR: API key configuration required. Please set GOOGLE_API_KEY in environment variables.")
        genai.configure(api_key=api_key)
        logger.success("API configuration completed successfully")

    def get_phase_examples(self, phase: Optional[str]) -> List[str]:
        logger.info(
            f"Retrieving phase examples for phase: {phase}")
        if not phase:
            examples = self.personality.get('example_interactions', [])
        else:
            arc = self.personality.get('hidden_story_arc', {})
            phase_data = arc.get(phase, {})
            examples = phase_data.get('examples', [])
        logger.info(f"Retrieved {len(examples)} example(s)")
        return examples

    def generate_tweet(self, topic: Optional[str] = None, phase: Optional[str] = None) -> str:
        logger.info(
            f"Initiating tweet generation process. Topic: {topic}, Phase: {phase}")
        has_intro = any(tweet.get('topic') ==
                        'introduction' for tweet in self.tweet_storage)
        if not has_intro:
            logger.info(
                "Generating initial introduction tweet")
            name = self.personality.get('name', 'Riley')
            description = self.personality.get('description', '')

            intro_prompt = f"""
            Write a friendly introduction tweet as {name}. This is the first tweet ever, so introduce yourself based on this description: {description}
            Make it warm, approachable, and excited to join the community. Keep it under {self.max_tweet_length} characters.
            Write in first person and make it feel genuine and personal.
            """

            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(intro_prompt)
                intro_tweet = response.candidates[0].content.parts[0].text.strip(
                )

                if len(intro_tweet) > self.max_tweet_length:
                    intro_tweet = intro_tweet[:self.max_tweet_length]

                tweet_entry = {
                    "text": intro_tweet,
                    "timestamp": datetime.now().isoformat(),
                    "topic": "introduction",
                    "phase": None
                }
                self.tweet_storage.append(tweet_entry)
                self.save_tweet_storage()

                logger.success(
                    "Introduction tweet generated and stored successfully")
                return intro_tweet
            except Exception as e:
                logger.error(
                    f"ERROR: Introduction tweet generation failed: {e}")
                return "ERROR: Tweet generation operation failed"
        elif has_intro:
            logger.info(
                "Initiating standard tweet generation process")
            name = self.personality.get('name', 'Riley')
            description = self.personality.get('description', '')
            examples = self.get_phase_examples(phase)
            games = self.game_types.get(topic, []) if topic else []

            full_prompt = f"""
            You are {name}, {description}.
            Write a casual, personal tweet as if you're sharing your genuine thoughts and experiences.
            Make it sound natural and conversational, like a real person talking to their friends.
            If mentioning games, reference these specific ones: {', '.join(games)}.
            Avoid sounding promotional or bot-like. Include real emotions, reactions, and relatable experiences.
            Keep it under {self.max_tweet_length} characters.
            
            Important: Write in first person, use natural language, and maybe even include some self-deprecating humor or personal anecdotes.
            """

            if examples:
                full_prompt += "\nHere are some example tweets for tone (but be original):\n"
                full_prompt += "\n".join(examples) + "\n"

            max_attempts = 3
            attempt = 0

            while attempt < max_attempts:
                try:
                    logger.info(
                        f"Executing generation attempt {attempt + 1} of {max_attempts}")
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(full_prompt)
                    generated_tweet = response.candidates[0].content.parts[0].text.strip(
                    )

                    if len(generated_tweet) > self.max_tweet_length:
                        generated_tweet = generated_tweet[:self.max_tweet_length]

                    if not self.is_similar_to_existing(generated_tweet):
                        tweet_entry = {
                            "text": generated_tweet,
                            "timestamp": datetime.now().isoformat(),
                            "topic": topic,
                            "phase": phase
                        }
                        self.tweet_storage.append(tweet_entry)
                        self.save_tweet_storage()
                        logger.info(
                            f"Tweet generated successfully: {generated_tweet}")
                        return generated_tweet

                    attempt += 1
                    logger.warning(
                        "WARNING: Generated tweet exceeded similarity threshold. Initiating new attempt")

                except Exception as e:
                    logger.critical(
                        f"CRITICAL ERROR: Tweet generation operation failed: {e}")
                    return f"ERROR: Tweet generation operation failed: {e}"

            logger.error(
                f"ERROR: Unable to generate unique tweet after {max_attempts} attempts")
            return "ERROR: Tweet generation operation failed. Please retry the operation."
