from bot.constants import start_quiz
from bot.di.dependency_injector import inject, Dependency
from bot.di.models import InjectionType
from bot.models import CommandContext, FlagCmd
from bot.svc.flag_quiz import FlagQuizSvc, FlagQuizInProgressException


@inject('flag_quiz_start', [
    Dependency.get('flag_quiz_svc', FlagQuizSvc, InjectionType.SINGLE_BY_TYPE)
])
class FlagQuizStart(FlagCmd):

    def __init__(self, flag_quiz_svc: FlagQuizSvc):
        self.flag_quiz_svc = flag_quiz_svc

    def is_applicable(self, ctx: CommandContext) -> bool:
        msg_lower = ctx.msg.content.lower()
        return msg_lower == start_quiz

    async def execute(self, ctx: CommandContext):
        try:
            self.flag_quiz_svc.start_new_quiz(ctx)
            question_text, flag_image = self.flag_quiz_svc.get_next_question(ctx)

            await ctx.msg.channel.send(f'Quiz starting in {self.flag_quiz_svc.time_between_questions} seconds...')
            await self.flag_quiz_svc.pause_quiz(ctx)
            await ctx.msg.channel.send(content=question_text, file=flag_image)

        except FlagQuizInProgressException:
            await ctx.msg.channel.send('Quiz in progress!')
