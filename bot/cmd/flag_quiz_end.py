from bot.const.constants import end_quiz_pattern
from bot.di.dependency_injector import Dependency, inject
from bot.di.models import InjectionType
from bot.models import CommandContext, FlagCmd
from bot.svc.flag_quiz import FlagQuizSvc, FlagQuizNoActiveQuizzesException
from bot.utils import matches


@inject('flag_quiz_end', [
    Dependency.get('flag_quiz_svc', FlagQuizSvc, InjectionType.SINGLE_BY_TYPE)
])
class FlagQuizEnd(FlagCmd):

    def __init__(self, flag_quiz_svc: FlagQuizSvc):
        self.flag_quiz_svc = flag_quiz_svc

    def is_applicable(self, ctx: CommandContext) -> bool:
        msg_lower = ctx.msg.content
        return matches(msg_lower, end_quiz_pattern)

    async def execute(self, ctx: CommandContext):
        try:
            leaderboard = self.get_leaderboard(ctx)
            self.flag_quiz_svc.end_quiz(ctx)
            await ctx.msg.channel.send(leaderboard)

        except FlagQuizNoActiveQuizzesException:
            await ctx.msg.channel.send('No active quizzes in this channel!')

    def get_leaderboard(self, ctx: CommandContext):
        quiz = self.flag_quiz_svc.get_quiz_by_ctx(ctx)
        if quiz is None:
            raise FlagQuizNoActiveQuizzesException()

        winners = sorted(quiz.user_scores.items(), key=lambda user_score: user_score[1], reverse=True)
        if len(winners) == 0:
            return 'There were no correct answers \u2013 and therefore no winners.'

        leaderboard = 'Leaderboard:\n'
        for i, (user, score) in enumerate(winners):
            leaderboard += f'{i + 1}. {user.mention} ({score})\n'

        return leaderboard
