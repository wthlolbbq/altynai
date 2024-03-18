from bot.constants import stutter_choices
from bot.di.dependency_injector import inject
from bot.di.models import Dependency, InjectionType
from bot.models import BaseCmd, CommandContext
from bot.svc.session_service import SessionSvc


@inject('stutter_chooser', [
    Dependency('session_svc', SessionSvc, InjectionType.BY_NAME)
])
class StutterChooser(BaseCmd):
    def __init__(self, session_svc: SessionSvc):
        self.session_svc = session_svc

    def is_applicable(self, ctx: CommandContext) -> bool:
        msg_lower = ctx.msg.content.lower()
        return msg_lower in stutter_choices

    async def execute(self, ctx: CommandContext):
        msg_lower = ctx.msg.content.lower()
        self.session_svc.is_stuttering = stutter_choices[msg_lower]
