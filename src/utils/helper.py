"""
Helper module for managing environment variables and logging functionality.

This module provides utilities for loading and retrieving environment variables
while maintaining detailed logging of all operations. It uses python-dotenv for
environment variable management and the built-in logging module for tracking
operations.

Functions:
    get_env_var(var_name): Retrieves the value of a specified environment variable.
"""

import os
import logging
from dotenv import load_dotenv

# Set up logging for utility-related actions
helper_logger = logging.getLogger("helper")
helper_logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/app.log")
handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
helper_logger.addHandler(handler)

# Load environment variables
load_dotenv()


def get_env_var(var_name):
    """
    Retrieve an environment variable.

    Args:
        var_name (str): The name of the environment variable to retrieve.

    Returns:
        str: The value of the environment variable.

    Raises:
        ValueError: If the environment variable is not found.

    Example:
        >>> api_key = get_env_var('API_KEY')
    """
    helper_logger.info(
        f"Attempting to retrieve environment variable: {var_name}")
    value = os.getenv(var_name)
    if value is None:
        helper_logger.error(f"Environment variable {var_name} not found.")
        raise ValueError(f"Environment variable {var_name} not found.")
    helper_logger.info(
        f"Environment variable {var_name} retrieved successfully.")
    return value
