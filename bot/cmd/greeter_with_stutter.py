import random

from bot.constants import greetings
from bot.di.dependency_injector import inject
from bot.di.models import Dependency, InjectionType
from bot.models import BaseCmd, CommandContext
from bot.svc.session_service import SessionSvc


@inject('greeter_with_stutter', [
    Dependency('session_svc', SessionSvc, InjectionType.BY_NAME)
])
class GreeterWithStutter(BaseCmd):

    def __init__(self, session_svc: SessionSvc):
        self.session_svc = session_svc

    def is_applicable(self, ctx: CommandContext) -> bool:
        msg_lower = ctx.msg.content.lower()
        return msg_lower in greetings and self.session_svc.is_stuttering

    async def execute(self, ctx: CommandContext):
        stutter: str = GreeterWithStutter.get_stutter(ctx)
        await ctx.msg.channel.send(stutter)

    @staticmethod
    def get_stutter(ctx, repeat_min=1, repeat_max=5) -> str:
        stutter_count = random.randint(repeat_min, repeat_max)
        stutter_letter = ctx.msg.content[0]
        stutter: str = (stutter_letter + '-') * stutter_count
        return stutter + ctx.msg.content.lower() + '~!'
