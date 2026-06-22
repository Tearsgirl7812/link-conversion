"""X (Twitter) URL Converter"""

from .base import BaseConverter


class XConverter(BaseConverter):
    """Convert X/Twitter URLs to clean format"""

    def convert(self, url: str) -> str:
        """Convert X/Twitter URL

        Removes tracking parameters like:
        - ?s=20
        - ?t=...
        - ?cn=...
        - etc.

        Also normalizes x.com vs twitter.com (prefers x.com).

        Args:
            url: X/Twitter URL

        Returns:
            Clean X/Twitter URL
        """
        # Remove all query parameters and fragments
        url = self.remove_query_params(url)

        # Normalize twitter.com to x.com
        url = url.replace('twitter.com', 'x.com')

        return url
