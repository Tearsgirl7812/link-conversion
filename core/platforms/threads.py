"""Threads URL Converter"""

from .base import BaseConverter


class ThreadsConverter(BaseConverter):
    """Convert Threads URLs to clean format"""

    def convert(self, url: str) -> str:
        """Convert Threads URL

        Removes tracking parameters from Threads URLs.

        Args:
            url: Threads URL

        Returns:
            Clean Threads URL
        """
        # Remove all query parameters and fragments
        return self.remove_query_params(url)
