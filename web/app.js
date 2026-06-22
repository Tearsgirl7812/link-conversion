/**
 * Link Conversion Tool - Web Application
 * Main JavaScript file
 */

// Configuration
const CONFIG = {
    API_URL: 'http://localhost:5000/api',
    USE_LOCAL: true, // Use local conversion if API unavailable
};

// Statistics
let stats = {
    convertedCount: 0,
    savedChars: 0,
};

// Load stats from localStorage
function loadStats() {
    const saved = localStorage.getItem('linkConversionStats');
    if (saved) {
        stats = JSON.parse(saved);
        updateStatsDisplay();
    }
}

// Save stats to localStorage
function saveStats() {
    localStorage.setItem('linkConversionStats', JSON.stringify(stats));
}

// Update stats display
function updateStatsDisplay() {
    document.getElementById('convertedCount').textContent = stats.convertedCount;
    document.getElementById('savedCharsCount').textContent = stats.savedChars;
}

// Platform detection
function detectPlatform(url) {
    const urlLower = url.toLowerCase();

    if (urlLower.includes('facebook.com')) return 'facebook';
    if (urlLower.includes('instagram.com')) return 'instagram';
    if (urlLower.includes('youtu')) return 'youtube';
    if (urlLower.includes('threads.net')) return 'threads';
    if (urlLower.includes('x.com') || urlLower.includes('twitter.com')) return 'x';

    return null;
}

// Local URL converters
const localConverters = {
    facebook(url) {
        return url.split('?')[0].split('#')[0];
    },
    instagram(url) {
        return url.split('?')[0].split('#')[0];
    },
    youtube(url) {
        // Handle youtu.be
        let match = url.match(/youtu\.be\/([a-zA-Z0-9_-]+)/);
        if (match) {
            return `https://www.youtube.com/watch?v=${match[1]}`;
        }

        // Handle youtube.com/watch
        match = url.match(/[?&]v=([a-zA-Z0-9_-]+)/);
        if (match) {
            return `https://www.youtube.com/watch?v=${match[1]}`;
        }

        // Handle youtube.com/embed
        match = url.match(/\/embed\/([a-zA-Z0-9_-]+)/);
        if (match) {
            return `https://www.youtube.com/watch?v=${match[1]}`;
        }

        return url.split('?')[0].split('#')[0];
    },
    threads(url) {
        return url.split('?')[0].split('#')[0];
    },
    x(url) {
        const cleaned = url.split('?')[0].split('#')[0];
        return cleaned.replace('twitter.com', 'x.com');
    },
};

// Convert URL
async function convertLink() {
    const inputUrl = document.getElementById('inputUrl').value.trim();

    if (!inputUrl) {
        showError('請貼上一個連結');
        return;
    }

    const platform = detectPlatform(inputUrl);

    if (!platform) {
        showError('不支持的平台。\n支持的平台: Facebook, Instagram, YouTube, Threads, X');
        return;
    }

    try {
        let convertedUrl;

        // Try API first, fallback to local
        if (!CONFIG.USE_LOCAL) {
            try {
                const response = await fetch(`${CONFIG.API_URL}/convert`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: inputUrl }),
                });

                const data = await response.json();

                if (!data.success) {
                    throw new Error(data.error);
                }

                convertedUrl = data.converted;
            } catch (apiError) {
                console.log('API unavailable, using local conversion');
                convertedUrl = localConverters[platform](inputUrl);
            }
        } else {
            convertedUrl = localConverters[platform](inputUrl);
        }

        // Show result
        showResult(inputUrl, convertedUrl, platform);

        // Update stats
        stats.convertedCount++;
        stats.savedChars += inputUrl.length - convertedUrl.length;
        saveStats();
        updateStatsDisplay();
    } catch (error) {
        showError(`轉換失敗: ${error.message}`);
    }
}

// Show result
function showResult(original, converted, platform) {
    hideError();

    const platformLabels = {
        facebook: '🔵 Facebook',
        instagram: '📷 Instagram',
        youtube: '🎥 YouTube',
        threads: '💬 Threads',
        x: '𝕏 X (Twitter)',
    };

    document.getElementById('platformBadge').textContent = platformLabels[platform] || platform;
    document.getElementById('originalUrl').textContent = original;
    document.getElementById('convertedUrl').textContent = converted;

    document.getElementById('resultSection').classList.remove('hidden');
}

// Show error
function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('errorSection').classList.remove('hidden');
}

// Hide error
function hideError() {
    document.getElementById('errorSection').classList.add('hidden');
}

// Copy URL to clipboard
function copyUrl(elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent;

    copyToClipboardText(text);
}

// Copy to clipboard
function copyToClipboard() {
    const text = document.getElementById('convertedUrl').textContent;
    copyToClipboardText(text);
}

// Helper: Copy text to clipboard
function copyToClipboardText(text) {
    if (navigator.clipboard) {
        navigator.clipboard
            .writeText(text)
            .then(() => {
                showNotification('✅ 已複製到剪貼板');
            })
            .catch(() => {
                fallbackCopy(text);
            });
    } else {
        fallbackCopy(text);
    }
}

// Fallback copy method
function fallbackCopy(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
    showNotification('✅ 已複製到剪貼板');
}

// Show notification
function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #10B981;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        z-index: 1000;
        animation: slideUp 0.3s ease-out;
        font-weight: 600;
    `;

    document.body.appendChild(notification);

    // Remove after 2 seconds
    setTimeout(() => {
        notification.remove();
    }, 2000);
}

// Open converted URL
function openConverted() {
    const url = document.getElementById('convertedUrl').textContent;
    window.open(url, '_blank');
}

// Clear all
function clearAll() {
    document.getElementById('inputUrl').value = '';
    document.getElementById('resultSection').classList.add('hidden');
    hideError();
    document.getElementById('inputUrl').focus();
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl+Enter or Cmd+Enter to convert
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        convertLink();
    }

    // Escape to clear
    if (e.key === 'Escape') {
        clearAll();
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    document.getElementById('inputUrl').focus();

    // Register service worker for PWA
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('sw.js').catch(() => {
            console.log('Service Worker registration failed');
        });
    }
});
