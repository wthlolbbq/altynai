from bot.const.constants import skip_quiz_pattern
from bot.di.dependency_injector import Dependency, inject
from bot.di.models import InjectionType
from bot.models import CommandContext, FlagCmd
from bot.svc.flag_quiz import FlagQuizSvc, FlagQuizNoActiveQuizzesException, FlagQuizNoActiveQuestionsException
from bot.utils import matches


@inject('flag_quiz_skip', [
    Dependency.get('flag_quiz_svc', FlagQuizSvc, InjectionType.SINGLE_BY_TYPE)
])
class FlagQuizSkip(FlagCmd):

    def __init__(self, flag_quiz_svc: FlagQuizSvc):
        self.flag_quiz_svc = flag_quiz_svc

    def is_applicable(self, ctx: CommandContext) -> bool:
        msg_content = ctx.msg.content
        return matches(msg_content, skip_quiz_pattern)

    async def execute(self, ctx: CommandContext):
        try:
            full_answer = self.flag_quiz_svc.reveal_answer(ctx)
            await ctx.msg.channel.send(f'The answer is **{full_answer}**!')
            await ctx.msg.channel.send(
                f'Question {self.flag_quiz_svc.get_question_num(ctx) + 1} in '
                f'{self.flag_quiz_svc.time_between_questions} seconds...'
            )
            await self.flag_quiz_svc.pause_quiz(ctx)
            question_text, attachment = self.flag_quiz_svc.get_next_question_data(ctx)
            await ctx.msg.channel.send(content=question_text, file=attachment)
        except FlagQuizNoActiveQuizzesException:
            await ctx.msg.channel.send('No active quizzes in this channel!')
        except FlagQuizNoActiveQuestionsException:
            await ctx.msg.channel.send('No active questions!')
