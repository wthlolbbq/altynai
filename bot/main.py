import os
from datetime import datetime

import discord  # NOQA
from discord import Intents, Client, Message  # NOQA
from dotenv import load_dotenv

from bot.constants import log_datetime_format
from bot.di.dependency_injector import get_injected_by_name
from bot.event.on_message import OnMessageHandler
from bot.event.on_ready import OnReadyHandler

load_dotenv()  # Assumes .env is present in the root directory.
TOKEN = os.getenv('DISCORD_TOKEN')

# bot setup
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(
    intents=intents
)


@client.event
async def on_ready() -> None:
    log_on_ready()

    on_ready_handler: OnReadyHandler = get_injected_by_name('on_ready')
    await on_ready_handler.handle(client)


@client.event
async def on_message(msg: Message) -> None:
    log_on_message(msg)

    on_message_handler: OnMessageHandler = get_injected_by_name('on_message')
    await on_message_handler.handle(msg, client)


def log_on_ready():
    print(f'{client.user} is now running.')


def log_on_message(msg):
    timestamp = datetime.utcnow().strftime(log_datetime_format)
    print(f'[{timestamp}] in {msg.channel} from {msg.author}: \"{msg.content}\"')


if __name__ == '__main__':
    client.run(token=TOKEN)
