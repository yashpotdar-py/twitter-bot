"""Helper module for environment variable management.

This module provides utility functions for loading and retrieving environment variables
with proper error handling and colored console output.
"""

import os
import sys
from dotenv import load_dotenv
from src.bot_logger.logger import Logger

project_root = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)


logger = Logger(__name__)
logger.info("Initializing helper module")

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
    logger.info(f"Initiating retrieval of environment variable: {var_name}")
    value = os.getenv(var_name)
    if value is None:
        error_msg = f"Environment variable {var_name} is not configured in the system."
        logger.error(f"ERROR: {error_msg}")
        raise ValueError(error_msg)
    logger.success(
        f"Environment variable {var_name} has been successfully retrieved")
    return value
