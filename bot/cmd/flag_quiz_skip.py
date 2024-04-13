from bot.constants import skip_quiz_pattern
from bot.di.dependency_injector import Dependency, inject
from bot.di.models import InjectionType
from bot.models import CommandContext, FlagCmd
from bot.svc.flag_quiz import FlagQuizSvc, FlagQuizNoActiveQuizzesException, FlagQuizNoActiveQuestionsException


@inject('flag_quiz_skip', [
    Dependency.get('flag_quiz_svc', FlagQuizSvc, InjectionType.SINGLE_BY_TYPE)
])
class FlagQuizSkip(FlagCmd):

    def __init__(self, flag_quiz_svc: FlagQuizSvc):
        self.flag_quiz_svc = flag_quiz_svc

    def is_applicable(self, ctx: CommandContext) -> bool:
        msg_content = ctx.msg.content
        return skip_quiz_pattern.search(msg_content) is not None

    async def execute(self, ctx: CommandContext):
        try:
            full_answer = self.flag_quiz_svc.reveal_answer(ctx)
            await ctx.msg.channel.send(f'The answer is **{full_answer}**!')
            await ctx.msg.channel.send(
                f'Question {self.flag_quiz_svc.get_question_num(ctx)} in '
                f'{self.flag_quiz_svc.time_between_questions} seconds...'
            )
            await self.flag_quiz_svc.pause_quiz(ctx)
            question_text, flag_image = self.flag_quiz_svc.get_next_question(ctx)
            await ctx.msg.channel.send(content=question_text, file=flag_image)
        except FlagQuizNoActiveQuizzesException:
            await ctx.msg.channel.send('No active quizzes in this channel!')
        except FlagQuizNoActiveQuestionsException:
            await ctx.msg.channel.send('No active questions!')
