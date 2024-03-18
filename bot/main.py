import os
import random
from datetime import datetime

import discord  # NOQA
from discord import Intents, Client, Message  # NOQA
from dotenv import load_dotenv

from bot.constants import entrance_lines, log_datetime_format
from bot.di.dependency_injector import get_injected_by_class
from bot.models import CommandContext, BaseCmd
from bot.utils import get_channel_by_name

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

    await greet_general_ch()


@client.event
async def on_message(msg: Message) -> None:
    log_on_message(msg)

    if msg.author != client.user:
        # Prevents responding to itself (the bot).
        await send_response(msg)


async def greet_general_ch():
    ch_general = get_channel_by_name(client, 'general')
    greeting = random.choice(entrance_lines)
    await ch_general.send(greeting)


async def send_response(msg: Message) -> None:
    ctx = CommandContext(msg, client)
    try:
        await next(i for i in get_injected_by_class(BaseCmd) if i.is_applicable(ctx)).execute(ctx)
    except StopIteration:
        pass
    except Exception as e:
        print(e)


def log_on_ready():
    print(f'{client.user} is now running.')


def log_on_message(msg):
    timestamp = datetime.utcnow().strftime(log_datetime_format)
    print(f'[{timestamp}] in {msg.channel} from {msg.author}: \"{msg.content}\"')


def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()
