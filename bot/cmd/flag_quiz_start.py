from bot.const.constants import start_quiz_pattern
from bot.di.dependency_injector import inject, Dependency
from bot.di.models import InjectionType
from bot.models import CommandContext, FlagCmd
from bot.svc.flag_quiz import FlagQuizSvc, FlagQuizInProgressException
from bot.utils import matches


@inject('flag_quiz_start', [
    Dependency.get('flag_quiz_svc', FlagQuizSvc, InjectionType.SINGLE_BY_TYPE)
])
class FlagQuizStart(FlagCmd):

    def __init__(self, flag_quiz_svc: FlagQuizSvc):
        self.flag_quiz_svc = flag_quiz_svc

    def is_applicable(self, ctx: CommandContext) -> bool:
        msg_content = ctx.msg.content
        return matches(msg_content, start_quiz_pattern)

    async def execute(self, ctx: CommandContext):
        try:
            self.flag_quiz_svc.start_new_quiz(ctx)
            await ctx.msg.channel.send(f'Question 1 in {self.flag_quiz_svc.time_between_questions} seconds...')
            await self.flag_quiz_svc.pause_quiz(ctx)
            question_text, attachment = self.flag_quiz_svc.get_next_question_data(ctx)
            await ctx.msg.channel.send(content=question_text, file=attachment)
        except FlagQuizInProgressException:
            await ctx.msg.channel.send('Quiz in progress!')
