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
import json
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from colorama import init, Fore, Style

init()

try:
    import google.generativeai as genai
except ImportError:
    print(f"{Fore.RED}Error: google-generativeai package is not installed. Please install it:")
    print("pip install google-generativeai{Style.RESET_ALL}")
    raise

load_dotenv()


class TweetGenerator:
    def __init__(self,
                 personality_filepath: str = 'src/ai/personality.json',
                 tweet_storage_filepath: str = 'src/ai/tweets.json',
                 max_tweet_length: int = 280,
                 similarity_threshold: float = 0.9):
        print(f"{Fore.CYAN}Initializing TweetGenerator...{Style.RESET_ALL}")
        self.personality = self.load_personality(personality_filepath)
        self.tweet_storage_filepath = tweet_storage_filepath
        self.max_tweet_length = max_tweet_length
        self.similarity_threshold = similarity_threshold
        self.configure_api()
        self.tweet_storage = self.load_tweet_storage()
        print(f"{Fore.GREEN}TweetGenerator initialized successfully{Style.RESET_ALL}")
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
        print(f"{Fore.BLUE}Loading personality from {filepath}...{Style.RESET_ALL}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                personality = json.load(f)
                print(
                    f"{Fore.GREEN}Personality loaded successfully{Style.RESET_ALL}")
                return personality
        except Exception as e:
            print(f"{Fore.RED}Error loading personality: {e}{Style.RESET_ALL}")
            raise ValueError(f"Failed to load personality: {e}")

    def load_tweet_storage(self) -> List[Dict]:
        print(f"{Fore.BLUE}Loading tweet storage...{Style.RESET_ALL}")
        if os.path.exists(self.tweet_storage_filepath):
            try:
                with open(self.tweet_storage_filepath, 'r', encoding='utf-8') as f:
                    tweets = json.load(f)
                    print(
                        f"{Fore.GREEN}Tweet storage loaded successfully{Style.RESET_ALL}")
                    return tweets
            except json.JSONDecodeError:
                print(
                    f"{Fore.YELLOW}Tweet storage file is empty or invalid{Style.RESET_ALL}")
                print("-" * 80)
                return []
        print(f"{Fore.YELLOW}Tweet storage file does not exist, starting with empty storage{Style.RESET_ALL}")
        print("-" * 80)
        return []

    def save_tweet_storage(self):
        print(f"{Fore.BLUE}Saving tweets to storage...{Style.RESET_ALL}")
        with open(self.tweet_storage_filepath, 'w', encoding='utf-8') as f:
            json.dump(self.tweet_storage, f, indent=4)
        print(f"{Fore.GREEN}Tweets saved successfully{Style.RESET_ALL}")

    def is_similar_to_existing(self, new_tweet: str) -> bool:
        print(f"{Fore.MAGENTA}Checking tweet similarity...{Style.RESET_ALL}")
        existing_tweets = [tweet['text'] for tweet in self.tweet_storage]
        if not existing_tweets:
            print(f"{Fore.YELLOW}No existing tweets to compare with{Style.RESET_ALL}")
            print("-" * 80)
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
        print(f"{Fore.CYAN}Similarity check result: {is_similar}{Style.RESET_ALL}")
        return is_similar

    def configure_api(self):
        print(f"{Fore.BLUE}Configuring API...{Style.RESET_ALL}")
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print(
                f"{Fore.RED}API key not found in environment variables{Style.RESET_ALL}")
            raise ValueError(
                "API key is required. Set GOOGLE_API_KEY in environment variables.")
        genai.configure(api_key=api_key)
        print(f"{Fore.GREEN}API configured successfully{Style.RESET_ALL}")

    def get_phase_examples(self, phase: Optional[str]) -> List[str]:
        print(f"{Fore.BLUE}Getting phase examples for: {phase}{Style.RESET_ALL}")
        if not phase:
            examples = self.personality.get('example_interactions', [])
        else:
            arc = self.personality.get('hidden_story_arc', {})
            phase_data = arc.get(phase, {})
            examples = phase_data.get('examples', [])
        print(f"{Fore.GREEN}Retrieved {len(examples)} examples{Style.RESET_ALL}")
        return examples

    def generate_tweet(self, topic: Optional[str] = None, phase: Optional[str] = None) -> str:
        print(
            f"{Fore.BLUE}Generating tweet for topic: {topic}, phase: {phase}{Style.RESET_ALL}")
        has_intro = any(tweet.get('topic') ==
                        'introduction' for tweet in self.tweet_storage)
        if not has_intro:
            print(f"{Fore.CYAN}Generating introduction tweet...{Style.RESET_ALL}")
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

                print(
                    f"{Fore.GREEN}Introduction tweet generated successfully{Style.RESET_ALL}")
                return intro_tweet
            except Exception as e:
                print(
                    f"{Fore.RED}Error occurred while generating introduction tweet: {e}{Style.RESET_ALL}")
                return "Error generating tweet"
        elif has_intro:
            print(f"{Fore.CYAN}Generating regular tweet...{Style.RESET_ALL}")
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
                    print(
                        f"{Fore.MAGENTA}Attempt {attempt + 1} of {max_attempts}{Style.RESET_ALL}")
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
                        print(f"{Fore.GREEN}Generated tweet:{Style.RESET_ALL}")
                        print(generated_tweet)
                        print("-" * 80)
                        return generated_tweet

                    attempt += 1
                    print(
                        f"{Fore.YELLOW}Tweet was too similar, trying again...{Style.RESET_ALL}")

                except Exception as e:
                    print(
                        f"{Fore.RED}Error occurred while generating tweet: {e}{Style.RESET_ALL}")
                    return f"Error generating tweet: {e}"

            print(
                f"{Fore.RED}Failed to generate a unique tweet after {max_attempts} attempts{Style.RESET_ALL}")
            return "Failed to generate a unique tweet. Please try again."


if __name__ == "__main__":
    print(f"{Fore.CYAN}Starting TweetGenerator test...{Style.RESET_ALL}")
    ai = TweetGenerator()
    test = ai.generate_tweet()
    print(test)
