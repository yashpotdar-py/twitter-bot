"""Helper module for environment variable management.

This module provides utility functions for loading and retrieving environment variables
with proper error handling and colored console output.
"""

import os
from dotenv import load_dotenv
from colorama import init, Fore

init()

load_dotenv()


def get_env_var(var_name):
    """Retrieve an environment variable with error handling and console feedback.

    Args:
        var_name (str): The name of the environment variable to retrieve.

    Returns:
        str: The value of the environment variable.

    Raises:
        ValueError: If the environment variable is not set.

    Example:
        >>> api_key = get_env_var('API_KEY')
    """
    print(f"{Fore.BLUE}[*] Attempting to get environment variable: {var_name}{Fore.RESET}")
    value = os.getenv(var_name)
    if value is None:
        error_msg = f"Environment variable {var_name} is not set."
        print(f"{Fore.RED}[!] Error: {error_msg}{Fore.RESET}")
        raise ValueError(error_msg)
    print(f"{Fore.GREEN}[+] Successfully retrieved environment variable: {var_name}{Fore.RESET}")
    return value