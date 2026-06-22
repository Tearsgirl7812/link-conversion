"""Discord Bot for Link Conversion"""

import os
import discord
from discord.ext import commands
import sys
import logging
from datetime import datetime

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

# Create bot
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    """Bot ready event"""
    logger.info(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name='for links to convert'
    ))


@bot.command(name='help')
async def help_command(ctx):
    """Help command"""
    embed = discord.Embed(
        title='🔗 Link Conversion Help',
        description='Convert social media links by removing tracking parameters',
        color=discord.Color.blue()
    )

    embed.add_field(
        name='How to Use',
        value='Simply share any supported social media link in a message, '
              'and I will automatically convert it to a clean link.',
        inline=False
    )

    embed.add_field(
        name='Supported Platforms',
        value='🔵 Facebook\n'
              '📷 Instagram\n'
              '🎥 YouTube\n'
              '💬 Threads\n'
              '𝕏 X (Twitter)',
        inline=False
    )

    embed.add_field(
        name='Example',
        value='**Input:** `https://www.instagram.com/p/ABC123/?utm_source=...`\n'
              '**Output:** `https://www.instagram.com/p/ABC123`',
        inline=False
    )

    embed.set_footer(text='🔒 All conversions are done locally - no data is collected')

    await ctx.send(embed=embed)


@bot.command(name='info')
async def info_command(ctx):
    """Bot information"""
    embed = discord.Embed(
        title='ℹ️ Link Conversion Bot',
        description='A Discord bot that removes tracking parameters from social media links',
        color=discord.Color.purple()
    )

    embed.add_field(name='Version', value='1.0.0', inline=True)
    embed.add_field(name='Platforms', value='5', inline=True)
    embed.add_field(
        name='Privacy',
        value='🔒 No data is collected or stored',
        inline=False
    )

    embed.set_footer(text=f'Created by Tearsgirl7812 | {datetime.now().strftime("%Y-%m-%d")}')

    await ctx.send(embed=embed)


@bot.event
async def on_message(message):
    """Handle incoming messages"""
    # Ignore bot's own messages
    if message.author == bot.user:
        await bot.process_commands(message)
        return

    # Check if message contains URL
    if not message.content.startswith('http'):
        await bot.process_commands(message)
        return

    try:
        result = converter.convert(message.content)

        if result['success']:
            platform_emoji = PLATFORM_EMOJIS.get(result['platform'], '🔗')
            embed = discord.Embed(
                title='✅ Link Converted',
                color=discord.Color.green()
            )

            embed.add_field(
                name='Platform',
                value=f'{platform_emoji} {result["platform"].upper()}',
                inline=False
            )

            embed.add_field(
                name='Original Link',
                value=f'```{result["original"]}```',
                inline=False
            )

            embed.add_field(
                name='Converted Link',
                value=f'```{result["converted"]}```',
                inline=False
            )

            await message.reply(embed=embed)

        else:
            embed = discord.Embed(
                title='❌ Conversion Failed',
                description=result['error'],
                color=discord.Color.red()
            )

            await message.reply(embed=embed)

    except Exception as e:
        embed = discord.Embed(
            title='❌ Error',
            description=str(e),
            color=discord.Color.red()
        )

        await message.reply(embed=embed)

    await bot.process_commands(message)


def main():
    """Start the bot"""
    token = os.getenv('DISCORD_TOKEN')

    if not token:
        raise ValueError('DISCORD_TOKEN environment variable is not set')

    bot.run(token)


if __name__ == '__main__':
    logger.info('Starting Discord bot...')
    main()
