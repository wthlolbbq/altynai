import random

from bot.const.constants import greetings, greeting_emojis
from bot.di.dependency_injector import inject, Dependency
from bot.di.models import InjectionType
from bot.models import BaseCmd, CommandContext
from bot.svc.session import SessionSvc


@inject('greeter', [
    Dependency.get('session_svc', SessionSvc, InjectionType.SINGLE_BY_TYPE)
])
class Greeter(BaseCmd):

    def __init__(self, session_svc: SessionSvc):
        self.session_svc = session_svc

    def is_applicable(self, ctx: CommandContext) -> bool:
        msg_lower = ctx.msg.content.lower()
        return msg_lower in greetings and not self.session_svc.is_stuttering

    async def execute(self, ctx: CommandContext):
        greeting = Greeter.get_greeting()
        await ctx.msg.channel.send(greeting)

    @staticmethod
    def get_greeting():
        greeting: str = random.choice(list(greetings))
        greeting = greeting[0].upper() + greeting[1:]
        emoji = random.choice(greeting_emojis)
        return f'{greeting}! {emoji}'
