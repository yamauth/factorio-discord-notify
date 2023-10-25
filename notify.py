import discord
import asyncio
import os
import shutil
import logging
from discord.ext import tasks
from dotenv import load_dotenv

# Initial dotenv
load_dotenv()

# Discord Bot Token
TOKEN = os.environ.get("TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
channel = None

# Factorio console-log path
console_log_path      = f'/opt/factorio/factorio/console-log'
console_log_path_prev = f'{console_log_path}.prev'

# Discord Client setting
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)

# Logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = 'notify.log',
    format = '%(asctime)s %(levelname)s %(message)s'
    )

@client.event
async def on_ready():
    global channel
    logging.info(f'Logged in as {client.user.name}')
    logging.info(f'Get Server: {client.guilds[0].name}(ID:{client.guilds[0].id})')
    channel = client.get_channel(int(CHANNEL_ID))
    logging.info(f'Get Channel: {channel}.')

    if not os.path.exists(console_log_path):
        raise FileNotFoundError(f'{console_log_path} is not exists')

    # when first run, make prev file
    if not os.path.exists(console_log_path_prev):
        shutil.copy(console_log_path, console_log_path_prev)

    loop.start()

@tasks.loop(seconds=10)
async def loop():
    await client.wait_until_ready()

    try:
        logging.info(f'Check Diff')

        # Diff current log and prev file
        # If new lines, send message
        with open(console_log_path, 'r') as current_file:
            current_lines = current_file.readlines()

        with open(console_log_path_prev, 'r') as prev_file:
            prev_lines = prev_file.readlines()

        search_strings = ['JOIN', 'LEAVE']
        new_lines = [
            line.strip()
            for line in current_lines
            if line not in prev_lines and any(search in line for search in search_strings)
        ]

        if len(new_lines) == 0:
            logging.info(f'No new lines')
            return

        logging.info(f'Add lines: {new_lines}')
        await channel.send('\n'.join(new_lines))

        shutil.copy(console_log_path, console_log_path_prev)

    except FileNotFoundError:
        pass

client.run(TOKEN)
