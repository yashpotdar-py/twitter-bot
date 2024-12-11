# src/utils/helpers.py
"""
Utility to retrieve the value of an environment variable.

Args:
    var_name (str): The name of the environment variable to retrieve.

Returns:
    str: The value of the environment variable.

Raises:
    ValueError: If the environment variable is not found.
"""
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()


def get_env_var(var_name):
    """Retrieve an environment variable."""
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Environment variable {var_name} not found.")
    return value


if __name__ == "__main__":
    # Print out all required environment variables for testing purposes
    print(f"""
CONSUMER_KEY = {get_env_var("CONSUMER_KEY")};
CONSUMER_SECRET = {get_env_var("CONSUMER_SECRET")};
ACCESS_TOKEN = {get_env_var("ACCESS_TOKEN")};
ACCESS_TOKEN_SECRET = {get_env_var("ACCESS_TOKEN_SECRET")};
""")
