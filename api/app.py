"""Flask API Server for Link Conversion"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.converter import LinkConverter

app = Flask(__name__)
CORS(app)

# Initialize converter
converter = LinkConverter()


class APIError(Exception):
    """Custom API Error"""

    def __init__(self, message, status_code=400):
        super().__init__()
        self.message = message
        self.status_code = status_code


@app.errorhandler(APIError)
def handle_api_error(error):
    """Handle API errors"""
    return jsonify({
        'success': False,
        'error': error.message
    }), error.status_code


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'version': '1.0.0'
    })


@app.route('/api/convert', methods=['POST'])
def convert():
    """Convert a URL

    Request body:
    {
        "url": "https://example.com/..."
    }

    Response:
    {
        "success": true,
        "platform": "platform_name",
        "original": "original_url",
        "converted": "converted_url"
    }
    """
    data = request.get_json()

    if not data:
        raise APIError('Request body must be JSON')

    url = data.get('url', '').strip()

    if not url:
        raise APIError('URL is required')

    result = converter.convert(url)

    if not result['success']:
        raise APIError(result.get('error', 'Conversion failed'), 400)

    return jsonify(result), 200


@app.route('/api/batch', methods=['POST'])
def batch_convert():
    """Convert multiple URLs

    Request body:
    {
        "urls": ["url1", "url2", ...]
    }

    Response:
    {
        "success": true,
        "results": [...]
    }
    """
    data = request.get_json()

    if not data:
        raise APIError('Request body must be JSON')

    urls = data.get('urls', [])

    if not isinstance(urls, list):
        raise APIError('URLs must be a list')

    if len(urls) == 0:
        raise APIError('At least one URL is required')

    if len(urls) > 100:
        raise APIError('Maximum 100 URLs per request')

    results = converter.batch_convert(urls)

    return jsonify({
        'success': True,
        'count': len(results),
        'results': results
    }), 200


@app.route('/api/detect', methods=['POST'])
def detect_platform():
    """Detect platform of a URL

    Request body:
    {
        "url": "https://example.com/..."
    }

    Response:
    {
        "success": true,
        "platform": "platform_name",
        "supported": true
    }
    """
    from core.detector import PlatformDetector

    data = request.get_json()

    if not data:
        raise APIError('Request body must be JSON')

    url = data.get('url', '').strip()

    if not url:
        raise APIError('URL is required')

    detector = PlatformDetector()
    platform = detector.detect(url)
    is_supported = detector.is_supported(url)

    return jsonify({
        'success': True,
        'url': url,
        'platform': platform.value,
        'supported': is_supported
    }), 200


@app.route('/api/info', methods=['GET'])
def info():
    """Get API information"""
    return jsonify({
        'name': 'Link Conversion API',
        'version': '1.0.0',
        'description': 'Clean social media links by removing tracking parameters',
        'platforms': [
            'facebook',
            'instagram',
            'youtube',
            'threads',
            'x'
        ],
        'endpoints': {
            'POST /api/convert': 'Convert a single URL',
            'POST /api/batch': 'Convert multiple URLs',
            'POST /api/detect': 'Detect platform of a URL',
            'GET /api/health': 'Health check',
            'GET /api/info': 'API information'
        }
    }), 200


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Link Conversion API Server')
    parser.add_argument('--host', default='0.0.0.0', help='Server host')
    parser.add_argument('--port', type=int, default=5000, help='Server port')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')

    args = parser.parse_args()

    print(f'Starting Link Conversion API on {args.host}:{args.port}')
    print('Visit http://localhost:5000/api/info for API documentation')

    app.run(host=args.host, port=args.port, debug=args.debug)
