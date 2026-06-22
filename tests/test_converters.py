"""Tests for Link Converters"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.converter import LinkConverter
from core.detector import PlatformDetector, Platform


class TestPlatformDetector:
    """Test platform detection"""

    def test_facebook_detection(self):
        """Test Facebook detection"""
        detector = PlatformDetector()
        assert detector.detect('https://facebook.com/share/p/123') == Platform.FACEBOOK
        assert detector.detect('https://fb.com/post/123') == Platform.FACEBOOK

    def test_instagram_detection(self):
        """Test Instagram detection"""
        detector = PlatformDetector()
        assert detector.detect('https://instagram.com/p/ABC123') == Platform.INSTAGRAM
        assert detector.detect('https://insta.com/reel/123') == Platform.INSTAGRAM

    def test_youtube_detection(self):
        """Test YouTube detection"""
        detector = PlatformDetector()
        assert detector.detect('https://youtube.com/watch?v=123') == Platform.YOUTUBE
        assert detector.detect('https://youtu.be/123') == Platform.YOUTUBE

    def test_threads_detection(self):
        """Test Threads detection"""
        detector = PlatformDetector()
        assert detector.detect('https://threads.net/t/123') == Platform.THREADS

    def test_x_detection(self):
        """Test X/Twitter detection"""
        detector = PlatformDetector()
        assert detector.detect('https://x.com/user/status/123') == Platform.X
        assert detector.detect('https://twitter.com/user/status/123') == Platform.X

    def test_unknown_detection(self):
        """Test unknown platform detection"""
        detector = PlatformDetector()
        assert detector.detect('https://example.com/page') == Platform.UNKNOWN
        assert not detector.is_supported('https://example.com/page')


class TestLinkConverter:
    """Test link converter"""

    def setup_method(self):
        """Setup test"""
        self.converter = LinkConverter()

    def test_instagram_conversion(self):
        """Test Instagram URL conversion"""
        url = 'https://www.instagram.com/p/DZQ_TWrlCRS/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ=='
        result = self.converter.convert(url)

        assert result['success']
        assert result['platform'] == 'instagram'
        assert result['converted'] == 'https://www.instagram.com/p/DZQ_TWrlCRS'

    def test_youtube_conversion_short(self):
        """Test YouTube short URL conversion"""
        url = 'https://youtu.be/iRSu_af96q8?si=UpTOo8--4Ca-h8P6'
        result = self.converter.convert(url)

        assert result['success']
        assert result['platform'] == 'youtube'
        assert result['converted'] == 'https://www.youtube.com/watch?v=iRSu_af96q8'

    def test_youtube_conversion_long(self):
        """Test YouTube long URL conversion"""
        url = 'https://www.youtube.com/watch?v=iRSu_af96q8&t=123s'
        result = self.converter.convert(url)

        assert result['success']
        assert result['platform'] == 'youtube'
        assert result['converted'] == 'https://www.youtube.com/watch?v=iRSu_af96q8'

    def test_x_conversion(self):
        """Test X/Twitter URL conversion"""
        url = 'https://x.com/user/status/123?s=20&t=abc'
        result = self.converter.convert(url)

        assert result['success']
        assert result['platform'] == 'x'
        assert result['converted'] == 'https://x.com/user/status/123'

    def test_threads_conversion(self):
        """Test Threads URL conversion"""
        url = 'https://threads.net/t/123?utm_source=share'
        result = self.converter.convert(url)

        assert result['success']
        assert result['platform'] == 'threads'
        assert result['converted'] == 'https://threads.net/t/123'

    def test_unsupported_platform(self):
        """Test unsupported platform"""
        url = 'https://example.com/page'
        result = self.converter.convert(url)

        assert not result['success']
        assert result['error'] == 'Unsupported platform'

    def test_invalid_url(self):
        """Test invalid URL"""
        result = self.converter.convert('')

        assert not result['success']
        assert result['error'] == 'Invalid URL provided'

    def test_batch_conversion(self):
        """Test batch URL conversion"""
        urls = [
            'https://www.instagram.com/p/ABC123/?utm_source=ig_web',
            'https://youtu.be/xyz123?si=abc',
        ]
        results = self.converter.batch_convert(urls)

        assert len(results) == 2
        assert results[0]['success']
        assert results[1]['success']
        assert results[0]['platform'] == 'instagram'
        assert results[1]['platform'] == 'youtube'

    def test_twitter_to_x_normalization(self):
        """Test Twitter URL normalized to X"""
        url = 'https://twitter.com/user/status/123'
        result = self.converter.convert(url)

        assert result['success']
        assert 'x.com' in result['converted']
