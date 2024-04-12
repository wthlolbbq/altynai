from bot.constants import end_quiz
from bot.di.dependency_injector import Dependency, inject
from bot.di.models import InjectionType
from bot.models import FlagCmd, CommandContext
from bot.svc.flag_quiz import FlagQuizSvc, FlagQuizNoActiveQuizzesException


@inject('flag_quiz_end', [
    Dependency.get('flag_quiz_svc', FlagQuizSvc, InjectionType.SINGLE_BY_TYPE)
])
class FlagQuizEnd(FlagCmd):

    def __init__(self, flag_quiz_svc: FlagQuizSvc):
        self.flag_quiz_svc = flag_quiz_svc

    def is_applicable(self, ctx: CommandContext) -> bool:
        msg_lower = ctx.msg.content.lower()
        return msg_lower == end_quiz

    async def execute(self, ctx: CommandContext):
        try:
            quiz = self.flag_quiz_svc.get_quiz_by_ctx(ctx)
            self.flag_quiz_svc.end_quiz(ctx)

            winners = sorted(quiz.user_scores.items(), key=lambda x: x[1], reverse=True)
            leaderboard = 'Leaderboard:\n'
            for i, (user, score) in enumerate(winners):
                leaderboard += f'{i+1}. {user.mention} ({score})\n'

            await ctx.msg.channel.send(leaderboard)

        except FlagQuizNoActiveQuizzesException:
            await ctx.msg.channel.send('No active quizzes in this channel!')
