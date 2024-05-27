from bot.const.constants import loveyou_pattern
from bot.di.dependency_injector import inject
from bot.models import CommandContext, BaseCmd
from bot.utils import matches


@inject('reactor')
class Reactor(BaseCmd):
    def is_applicable(self, ctx: CommandContext) -> bool:
        msg_content = ctx.msg.content
        return matches(msg_content, loveyou_pattern)

    async def execute(self, ctx: CommandContext):
        await ctx.msg.add_reaction(Reactor.get_reaction())

    @staticmethod
    def get_reaction():
        return '❤️'
