from bot.constants import loveyou_re
from bot.di.dependency_injector import inject
from bot.models import CommandContext, BaseCmd


@inject('reactor', [])
class Reactor(BaseCmd):
    def is_applicable(self, ctx: CommandContext) -> bool:
        msg_content = ctx.msg.content
        return loveyou_re.search(msg_content) is not None

    async def execute(self, ctx: CommandContext):
        await ctx.msg.add_reaction(Reactor.get_reaction())

    @staticmethod
    def get_reaction():
        return '❤️'
