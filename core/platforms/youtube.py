"""YouTube URL Converter"""

import re
from urllib.parse import urlparse, parse_qs
from .base import BaseConverter


class YouTubeConverter(BaseConverter):
    """Convert YouTube URLs to clean standard format"""

    def convert(self, url: str) -> str:
        """Convert YouTube URL to standard youtube.com/watch?v={id} format

        Handles:
        - youtu.be/{id}
        - youtube.com/watch?v={id}
        - youtube.com/embed/{id}
        - youtube.com/v/{id}

        Args:
            url: YouTube URL

        Returns:
            Standard YouTube URL
        """
        video_id = self._extract_video_id(url)

        if not video_id:
            # If we can't extract ID, return URL without parameters
            return self.remove_query_params(url)

        return f'https://www.youtube.com/watch?v={video_id}'

    @staticmethod
    def _extract_video_id(url: str) -> str:
        """Extract video ID from various YouTube URL formats

        Args:
            url: YouTube URL

        Returns:
            Video ID or empty string
        """
        # youtu.be/{id}
        match = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', url)
        if match:
            return match.group(1)

        # youtube.com/watch?v={id}
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        if 'v' in params:
            return params['v'][0]

        # youtube.com/embed/{id}
        match = re.search(r'/embed/([a-zA-Z0-9_-]+)', url)
        if match:
            return match.group(1)

        # youtube.com/v/{id}
        match = re.search(r'/v/([a-zA-Z0-9_-]+)', url)
        if match:
            return match.group(1)

        return ''
