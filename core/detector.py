"""Platform Detection Module"""

from enum import Enum
from typing import Optional


class Platform(Enum):
    """Supported social media platforms"""
    FACEBOOK = 'facebook'
    INSTAGRAM = 'instagram'
    YOUTUBE = 'youtube'
    THREADS = 'threads'
    X = 'x'
    UNKNOWN = 'unknown'


class PlatformDetector:
    """Detect which platform a URL belongs to"""

    PLATFORM_PATTERNS = {
        Platform.FACEBOOK: [
            'facebook.com',
            'fb.com',
        ],
        Platform.INSTAGRAM: [
            'instagram.com',
            'insta.com',
        ],
        Platform.YOUTUBE: [
            'youtube.com',
            'youtu.be',
            'yt.be',
        ],
        Platform.THREADS: [
            'threads.net',
        ],
        Platform.X: [
            'x.com',
            'twitter.com',
        ],
    }

    @classmethod
    def detect(cls, url: str) -> Platform:
        """Detect platform from URL

        Args:
            url: The URL to detect

        Returns:
            Platform enum value
        """
        url_lower = url.lower()

        for platform, patterns in cls.PLATFORM_PATTERNS.items():
            for pattern in patterns:
                if pattern in url_lower:
                    return platform

        return Platform.UNKNOWN

    @classmethod
    def is_supported(cls, url: str) -> bool:
        """Check if URL platform is supported"""
        return cls.detect(url) != Platform.UNKNOWN
