"""Main Link Converter Module"""

from typing import Dict, Any
from .detector import PlatformDetector, Platform
from .platforms import (
    FacebookConverter,
    InstagramConverter,
    YouTubeConverter,
    ThreadsConverter,
    XConverter,
)


class LinkConverter:
    """Main converter that routes to platform-specific converters"""

    CONVERTERS = {
        Platform.FACEBOOK: FacebookConverter,
        Platform.INSTAGRAM: InstagramConverter,
        Platform.YOUTUBE: YouTubeConverter,
        Platform.THREADS: ThreadsConverter,
        Platform.X: XConverter,
    }

    def __init__(self):
        """Initialize converter"""
        self.detector = PlatformDetector()
        self.converters = {k: v() for k, v in self.CONVERTERS.items()}

    def convert(self, url: str) -> Dict[str, Any]:
        """Convert a URL

        Args:
            url: The URL to convert

        Returns:
            Dict with keys:
                - 'success': bool
                - 'platform': str
                - 'original': str
                - 'converted': str (if success)
                - 'error': str (if failed)
        """
        if not url or not isinstance(url, str):
            return {
                'success': False,
                'error': 'Invalid URL provided',
                'platform': 'unknown'
            }

        url = url.strip()
        platform = self.detector.detect(url)

        if platform == Platform.UNKNOWN:
            return {
                'success': False,
                'error': 'Unsupported platform',
                'platform': 'unknown',
                'original': url
            }

        converter = self.converters[platform]

        try:
            converted = converter.convert(url)
            return {
                'success': True,
                'platform': platform.value,
                'original': url,
                'converted': converted
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'platform': platform.value,
                'original': url
            }

    def batch_convert(self, urls: list) -> list:
        """Convert multiple URLs

        Args:
            urls: List of URLs to convert

        Returns:
            List of conversion results
        """
        return [self.convert(url) for url in urls]
