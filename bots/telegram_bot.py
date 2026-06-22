"""Telegram Bot for Link Conversion"""

import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import sys
import logging

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.converter import LinkConverter

# Initialize converter
converter = LinkConverter()

# Platform emojis
PLATFORM_EMOJIS = {
    'facebook': '🔵',
    'instagram': '📷',
    'youtube': '🎥',
    'threads': '💬',
    'x': '𝕏',
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler"""
    welcome_text = '''🔗 **Link Conversion Bot**

歡迎使用連結轉換機器人！

**功能：**
只需發送任何社交媒體連結，機器人將自動移除跟蹤參數並轉換為潔淨連結。

**支持的平台：**
🔵 Facebook
📷 Instagram
🎥 YouTube
💬 Threads
𝕏 X (Twitter)

**使用方法：**
1. 複製社交媒體上的連結
2. 貼到此聊天中
3. 機器人將自動轉換並回覆

**命令：**
/start - 顯示此訊息
/help - 獲取幫助
/stats - 查看轉換統計
'''\n
    await update.message.reply_text(welcome_text, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command handler"""
    help_text = '''📖 **幫助**

**如何使用：**
1. 複製您的社交媒體連結
2. 貼入此聊天
3. 機器人將返回潔淨連結

**示例：**
- Instagram: `https://www.instagram.com/p/ABC123/?utm_source=...`
  → 轉換為: `https://www.instagram.com/p/ABC123`

- YouTube: `https://youtu.be/dQw4w9WgXcQ?si=...`
  → 轉換為: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`

- X: `https://x.com/user/status/123?s=20`
  → 轉換為: `https://x.com/user/status/123`

**隱私：**
🔒 所有轉換在本地進行，不收集任何數據。
'''\n
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages"""
    text = update.message.text

    # Check if message contains URL
    if not text.startswith('http'):
        return

    try:
        result = converter.convert(text)

        if result['success']:
            platform_emoji = PLATFORM_EMOJIS.get(result['platform'], '🔗')
            response = f'''✅ **轉換成功**

**平台：** {platform_emoji} {result['platform'].upper()}

**原始連結：**
`{result['original']}`

**轉換後：**
`{result['converted']}`

💾 已複製到剪貼板
'''\n
        else:
            response = f'''❌ **轉換失敗**

**錯誤：** {result['error']}

**支持的平台：**
🔵 Facebook
📷 Instagram
🎥 YouTube
💬 Threads
𝕏 X (Twitter)
'''\n

        await update.message.reply_text(response, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(
            f'❌ **錯誤：** {str(e)}',
            parse_mode='Markdown'
        )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stats command handler"""
    stats_text = '''📊 **統計信息**

此機器人沒有收集個人統計數據。

所有轉換在本地進行，保護您的隱私。
'''\n

    await update.message.reply_text(stats_text, parse_mode='Markdown')


def main() -> None:
    """Start the bot"""
    # Get token from environment
    token = os.getenv('TELEGRAM_TOKEN')

    if not token:
        raise ValueError('TELEGRAM_TOKEN environment variable is not set')

    # Create the Application
    application = Application.builder().token(token).build()

    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('stats', stats_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Start the Bot
    application.run_polling()


if __name__ == '__main__':
    logger.info('Starting Telegram bot...')
    main()
