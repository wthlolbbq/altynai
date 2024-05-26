from bot.const.constants import stutter_choices
from bot.di.dependency_injector import inject, Dependency
from bot.di.models import InjectionType
from bot.models import BaseCmd, CommandContext
from bot.svc.session import SessionSvc


@inject('stutter_chooser', [
    Dependency.get('session_svc', SessionSvc, InjectionType.SINGLE_BY_TYPE)
])
class StutterChooser(BaseCmd):
    def __init__(self, session_svc: SessionSvc):
        self.session_svc = session_svc

    def is_applicable(self, ctx: CommandContext) -> bool:
        msg_lower = ctx.msg.content.lower()
        return msg_lower in stutter_choices

    async def execute(self, ctx: CommandContext):
        self.set_stutter_choice(ctx)

    def set_stutter_choice(self, ctx: CommandContext):
        new_stutter_choice = self.get_stutter_choice(ctx)
        self.session_svc.is_stuttering = new_stutter_choice

    def get_stutter_choice(self, ctx):
        msg_lower = ctx.msg.content.lower()
        return stutter_choices[msg_lower]
