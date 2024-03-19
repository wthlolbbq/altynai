import random

from discord import Client

from bot.constants import entrance_lines
from bot.di.dependency_injector import inject
from bot.models import BaseEvent
from bot.utils import get_channel_by_name


@inject('on_ready')
class OnReadyHandler(BaseEvent):

    async def handle(self, client: Client):
        await self.greet_general_ch(client)

    @staticmethod
    async def greet_general_ch(client: Client):
        greeting = random.choice(entrance_lines)
        ch_general = get_channel_by_name(client, 'general')
        await ch_general.send(greeting)
