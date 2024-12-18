import os
import sys
import codecs
import logging
import traceback
from typing import Optional
from logging.handlers import RotatingFileHandler


class Logger:
    """
    Enhanced logging utility with improved exception handling and color support.
    """

    def __init__(
        self,
        feature_name: str,
        log_level: int = logging.INFO,
        log_dir: str = 'logs',
        max_log_size: int = 1024 * 1024,
        backup_count: int = 3,
        console_enabled: bool = True
    ):
        """
        Initialize a logger with comprehensive configuration options.
        """
        try:
            os.makedirs(log_dir, exist_ok=True)
        except PermissionError:
            print(
                f"Error: No permission to create log directory in {os.getcwd()}")
            raise

        self.logger = logging.getLogger(feature_name)
        self.logger.setLevel(log_level)
        self.logger.handlers.clear()

        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        log_file_path = os.path.join(log_dir, f'{feature_name}.log')
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=max_log_size,
            backupCount=backup_count
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        if console_enabled:
            console_handler = logging.StreamHandler(codecs.getwriter('utf-8')(sys.stdout.buffer))
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

    def _format_log_message(self, prefix: str, message: str, is_console: bool = False) -> str:
        """
        Create a consistently formatted log message with color and prefix.

        Args:
            prefix (str): Log message prefix
            message (str): Main log message
            is_console (bool): Whether the message is for console output

        Returns:
            str: Formatted, colored log message
        """
        if is_console:
            colors = {
                "INFORMATION:": "\033[96m",          # Cyan
                "SUCCESS:": "\033[92m",              # Lime
                "WARNING:": "\033[93m",              # Yellow
                "ERROR:": "\033[91m",                # Red
                "CRITICAL:": "\033[91;1m",           # Bright Red
                "EXCEPTION:": "\033[91m",            # Red
                "EXCEPTION DETAILS:": "\033[91m",    # Red
                "CRITICAL EXCEPTION:": "\033[91;1m"  # Bright Red
            }
            reset_color = "\033[0m"
            color = colors.get(prefix, "")
            return f"{color}{prefix} {message}{reset_color}"
        return f"{prefix} {message}"

    def info(self, message: str) -> None:
        """Log an informational message."""
        self.logger.info(self._format_log_message(
            "INFORMATION:", message, False))
        if self.logger.handlers and isinstance(self.logger.handlers[-1], logging.StreamHandler):
            print(self._format_log_message("INFORMATION:", message, True))

    def success(self, message: str) -> None:
        """Log a success message."""
        self.logger.info(self._format_log_message("SUCCESS:", message, False))
        if self.logger.handlers and isinstance(self.logger.handlers[-1], logging.StreamHandler):
            print(self._format_log_message("SUCCESS:", message, True))

    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(self._format_log_message(
            "WARNING:", message, False))
        if self.logger.handlers and isinstance(self.logger.handlers[-1], logging.StreamHandler):
            print(self._format_log_message("WARNING:", message, True))

    def error(self, message: str, exc: Optional[Exception] = None, include_traceback: bool = False) -> None:
        """
        Log an error message with optional exception details and traceback.

        Args:
            message (str): The error message to log
            exc (Optional[Exception], optional): Optional exception for additional context
            include_traceback (bool, optional): Whether to include full traceback. Defaults to True.
        """
        self.logger.error(self._format_log_message("ERROR:", message, False))
        if self.logger.handlers and isinstance(self.logger.handlers[-1], logging.StreamHandler):
            print(self._format_log_message("ERROR:", message, True))

        if exc:
            if include_traceback:
                tb_message = self._format_log_message(
                    "EXCEPTION DETAILS:", f"\n{traceback.format_exc()}", False)
                self.logger.error(tb_message)
                if self.logger.handlers and isinstance(self.logger.handlers[-1], logging.StreamHandler):
                    print(self._format_log_message("EXCEPTION DETAILS:",
                          f"\n{traceback.format_exc()}", True))
            else:
                exc_message = self._format_log_message(
                    "EXCEPTION:", f"{str(exc)}", False)
                self.logger.error(exc_message)
                if self.logger.handlers and isinstance(self.logger.handlers[-1], logging.StreamHandler):
                    print(self._format_log_message(
                        "EXCEPTION:", f"{str(exc)}", True))

    def critical(self, message: str, exc: Optional[Exception] = None) -> None:
        """
        Log a critical message with optional exception details.

        Args:
            message (str): The critical message to log
            exc (Optional[Exception], optional): Optional exception for additional context
        """
        self.logger.critical(self._format_log_message(
            "CRITICAL:", message, False))
        if self.logger.handlers and isinstance(self.logger.handlers[-1], logging.StreamHandler):
            print(self._format_log_message("CRITICAL:", message, True))

        if exc:
            exc_message = self._format_log_message(
                "CRITICAL EXCEPTION:", f"{traceback.format_exc()}", False)
            self.logger.critical(exc_message)
            if self.logger.handlers and isinstance(self.logger.handlers[-1], logging.StreamHandler):
                print(self._format_log_message(
                    "CRITICAL EXCEPTION:", f"{traceback.format_exc()}", True))

    def __enter__(self):
        """Support for context manager protocol."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Handle logging of exceptions when used as a context manager.

        Returns False to propagate any exceptions that occurred.
        """
        if exc_type:
            self.error(
                f"An exception of type {exc_type.__name__} has occurred", exc_val)
        return False
