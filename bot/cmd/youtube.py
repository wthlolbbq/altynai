import random

from bot.constants import youtube_pattern, rickroll_url
from bot.di.dependency_injector import inject
from bot.models import BaseCmd, CommandContext
from bot.utils import matches


@inject('youtube')
class YouTubeSearch(BaseCmd):
    def is_applicable(self, ctx: CommandContext) -> bool:
        msg_lower = ctx.msg.content.lower()
        return matches(msg_lower, youtube_pattern)

    async def execute(self, ctx: CommandContext):
        message = self.get_youtube_result_message(ctx)
        await ctx.msg.channel.send(message)

    def get_youtube_result_message(self, ctx):
        result_count = random.randint(5, 303)
        msg_lower = ctx.msg.content
        search_term = youtube_pattern.search(msg_lower)['search_term']
        return (f'Found {result_count} matches for \'{search_term}\'. ' +
                f'First result: <{rickroll_url}>')
