import discord  # NOQA

from bot.cmd.flag_quiz_start import FlagQuizSvc
from bot.di.dependency_injector import inject, Dependency
from bot.di.models import InjectionType
from bot.helper.ordered import HIGH_PRIORITY
from bot.models import CommandContext, FlagCmd


@inject('flag_quiz', [
    Dependency.get('flag_quiz_svc', FlagQuizSvc, InjectionType.SINGLE_BY_TYPE)
])
class FlagQuizAttempt(FlagCmd):

    def __init__(self, flag_quiz_svc: FlagQuizSvc):
        self.flag_quiz_svc = flag_quiz_svc

    def is_applicable(self, ctx: CommandContext) -> bool:
        return self.flag_quiz_svc.quiz_in_progress(ctx)

    async def execute(self, ctx: CommandContext):
        if self.flag_quiz_svc.try_answer(ctx):
            full_answer = self.flag_quiz_svc.get_quiz_by_ctx(ctx).question.full_answer
            await ctx.msg.channel.send(f'{ctx.msg.author.mention} Correct, that\'s **{full_answer}**!')
            await ctx.msg.channel.send(f'Next question in {self.flag_quiz_svc.time_between_questions} seconds...')
            await self.flag_quiz_svc.pause_quiz(ctx)
            question_text, flag_image = self.flag_quiz_svc.get_next_question(ctx)
            await ctx.msg.channel.send(content=question_text, file=flag_image)

    def get_priority(self):
        return HIGH_PRIORITY
