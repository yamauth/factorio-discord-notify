import discord
import asyncio
import os
import shutil
import subprocess
import logging
from os.path import join, dirname
from discord.ext import tasks
from dotenv import load_dotenv

# Initial dotenv
load_dotenv()

# Discord Bot Token
TOKEN = os.environ.get("TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
channel = None

# Factorio console-log path
console_log_path      = '/opt/factorio/factorio/console-log'
console_log_path_prev = '{console_log_path}.prev'

# Discord Client setting
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)

# Logging
logging.basicConfig(
    level=logging.DEBUG,
    filename='discord-notify.log',
    format='%(asctime)s %(levelname)s %(message)s'
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
    global last_modified
    await client.wait_until_ready()

    try:
        logging.info(f'Check Diff')

        # Diff current log and prev file
        # If add lines, send message
        with open(console_log_path, 'r') as current_file, open(console_log_path_prev, 'r') as prev_file:
            search_strings = ['JOIN', 'LEAVE']
            add_lines = [
                line
                for line in set(prev_file.readlines()) - set(current_file.readlines())
                if any(search in line for search in search_strings)
            ]

            if len(add_lines) == 0:
                logging.info(f'No new lines')
                return

            logging.info(f'Add lines: {add_lines}')
            await channel.send(add_lines)

            shutil.copy(console_log_path, console_log_path_prev)

    except FileNotFoundError:
        pass

client.run(TOKEN)
