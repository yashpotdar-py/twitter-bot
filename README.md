# Twitter Bot

A sophisticated Twitter bot that generates and posts tweets with a unique personality named Riley. The bot uses Google's Generative AI to create authentic, personality-driven content while maintaining contextual awareness across different gaming topics.

---

## Features

- **Automated Tweet Generation**: Utilizes Google's Generative AI to create engaging tweets.
- **Personality-Driven Content**: Develops a unique character (Riley) with evolving personality traits and preferences.
- **Contextual Awareness**: Tailors tweets based on different gaming topics.
- **Tweet Similarity Checking**: Ensures tweets are unique by checking for duplicates.
- **OAuth Authentication Handling**: Manages secure Twitter login and authentication.
- **Automated Browser Interaction**: Uses Selenium for automated Twitter authentication.
- **Persistent Tweet Storage**: Stores generated tweets locally for easy management.
- **Colored Console Output**: Enhances visibility with color-coded console logs.
- **Debug Mode Support**: Allows you to run the bot in debug mode for troubleshooting.

---

## Prerequisites

Before running the bot, ensure you have the following:

- Python 3.8+ installed
- Google AI API key (for tweet generation)
- Twitter Developer Account (for API credentials)
- Chrome browser installed

---

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yashpotdar-py/twitter-bot.git
   cd twitter-bot
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:

   Create a `.env` file in the root directory and add the following variables:

   ```python
   BEARER_TOKEN=<your_bearer_token>
   CONSUMER_KEY=<your_consumer_key>
   CONSUMER_SECRET=<your_consumer_secret>
   ACCESS_TOKEN=<your_access_token>
   ACCESS_TOKEN_SECRET=<your_access_token_secret>
   CLIENT_ID=<your_client_id>
   CLIENT_SECRET=<your_client_secret>
   TWITTER_USERNAME=<your_twitter_username>
   TWITTER_PASSWORD=<your_twitter_password>
   TWITTER_EMAIL=<your_twitter_email>
   GOOGLE_API_KEY=<your_google_api_key>
   ```

4. **Run the bot**:

   ```bash
   python app.py
   ```

5. **Run in debug mode** (optional):

   ```bash
   python app.py --debug
   ```

---

## Project Structure

Here's a quick overview of the project's structure:

```bash
twitter-bot/
├── app.py                      # Main application entry point
├── src/                        # AI-related components
│   ├── ai/                     # AI-related components
│   │   └── tweet_generator.py  # Tweet generation logic
│   └── personality.json        # Character profile and story arc
│   └── tweets.json             # Stored tweets
├── auth/                       # Authentication handling
│   └── oauth_handler.py        # Twitter OAuth implementation
├── twitter/                    # Twitter API interaction
│   └── post_tweet.py           # Tweet posting functionality
├── utils/                      # Utility functions
│   └── helper.py               # Environment variable management
├── selenium_setup.py           # Browser automation setup
├── requirements.txt            # Python dependencies
└── .env                        # Environment variables
```

---

## Features in Detail

### Tweet Generation
- **Contextual Awareness**: The bot generates tweets based on various gaming topics, keeping each tweet relevant and engaging.
- **Personality-Driven Content**: Riley’s personality evolves, and the bot incorporates this development into its tweets.
- **Story Arc Progression**: The bot's tweets reflect the growth and changes in Riley’s character, creating a deeper narrative over time.
- **Duplicate Content Prevention**: The bot ensures each tweet is unique and avoids repeating content.
- **Phase-Based Content Generation**: Tweets are categorized into phases, ensuring content aligns with the current stage of Riley’s development.

### Authentication
- **Automated OAuth Flow**: Handles secure authentication with Twitter using OAuth credentials.
- **Browser Automation**: Uses Selenium WebDriver for automated browser interaction and login.

### Tweet Management
- **Persistent Storage**: Tweets are stored locally in a JSON file for future reference and potential re-use.
- **Similarity Checking**: The bot checks for similar or duplicate tweets before posting.
- **Topic Categorization**: Tweets are categorized based on the gaming subject matter to ensure relevant content.
- **Phase-Based Content Generation**: Tweets change depending on the current narrative phase, keeping them fresh and engaging.

---

## Contributing

We welcome contributions! If you would like to contribute to the project, please follow these steps:

1. **Fork the repository**
2. **Create your feature branch**
3. **Commit your changes**
4. **Push to your branch**
5. **Create a Pull Request**

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

- **Google Generative AI**: For powerful tweet generation.
- **Twitter API**: For handling Twitter interactions.
- **Selenium WebDriver**: For automating Twitter login and browser interactions.

---

Feel free to fork, contribute, or improve the bot to your liking! We hope Riley can bring some fun to your Twitter feed.

---

### Contact

If you have any questions or suggestions, feel free to reach out via Twitter or open an issue on GitHub.

---