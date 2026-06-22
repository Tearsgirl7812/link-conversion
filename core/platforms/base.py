"""Base converter class"""

from abc import ABC, abstractmethod
from urllib.parse import urlparse, parse_qs
import re


class BaseConverter(ABC):
    """Base class for platform converters"""

    @abstractmethod
    def convert(self, url: str) -> str:
        """Convert URL to clean format

        Args:
            url: The URL to convert

        Returns:
            Cleaned URL
        """
        pass

    @staticmethod
    def remove_query_params(url: str) -> str:
        """Remove query parameters from URL

        Args:
            url: The URL to clean

        Returns:
            URL without query parameters
        """
        return url.split('?')[0].split('#')[0]

    @staticmethod
    def get_query_param(url: str, param: str) -> str:
        """Get specific query parameter value

        Args:
            url: The URL
            param: Parameter name

        Returns:
            Parameter value or empty string
        """
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        return params.get(param, [''])[0]

    @staticmethod
    def extract_regex(url: str, pattern: str) -> str:
        """Extract value using regex pattern

        Args:
            url: The URL
            pattern: Regex pattern with capture group

        Returns:
            Captured value or empty string
        """
        match = re.search(pattern, url)
        return match.group(1) if match else ''
