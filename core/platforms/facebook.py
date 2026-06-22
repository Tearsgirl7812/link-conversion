"""Facebook URL Converter"""

import re
from .base import BaseConverter


class FacebookConverter(BaseConverter):
    """Convert Facebook URLs to clean format"""

    def convert(self, url: str) -> str:
        """Convert Facebook URL

        Handles:
        - facebook.com/share/p/{id}
        - facebook.com/{user}/posts/{id}
        - facebook.com/photo.php?fbid={id}

        Args:
            url: Facebook URL

        Returns:
            Clean Facebook URL
        """
        # Remove query parameters and fragments
        url = self.remove_query_params(url)

        # Handle /share/p/ format
        share_match = re.search(r'/share/p/([^/]+)', url)
        if share_match:
            # For share links, return as-is (without params)
            # In production, you might want to fetch the actual post URL
            return url

        # Handle /photo.php?fbid= format
        fbid_match = re.search(r'fbid=([0-9]+)', url)
        if fbid_match:
            fbid = fbid_match.group(1)
            return f'https://www.facebook.com/photo.php?fbid={fbid}'

        # Default: return without parameters
        return url
