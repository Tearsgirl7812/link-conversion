"""Instagram URL Converter"""

import re
from .base import BaseConverter


class InstagramConverter(BaseConverter):
    """Convert Instagram URLs to clean format"""

    def convert(self, url: str) -> str:
        """Convert Instagram URL

        Removes tracking parameters like:
        - utm_source
        - utm_medium
        - utm_campaign
        - igsh
        - etc.

        Args:
            url: Instagram URL

        Returns:
            Clean Instagram URL
        """
        # Remove all query parameters
        url = self.remove_query_params(url)

        # Handle various Instagram URL formats
        # /p/, /reel/, /tv/, /stories/
        patterns = [
            r'(https?://(?:www\.)?instagram\.com/(?:p|reel|tv|stories)/[^/?]+)',
            r'(https?://(?:www\.)?instagram\.com/([a-zA-Z0-9_.]+))',
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return url
