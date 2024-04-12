from bot.constants import end_quiz_pattern
from bot.di.dependency_injector import Dependency, inject
from bot.di.models import InjectionType
from bot.models import CommandContext, FlagCmd
from bot.svc.flag_quiz import FlagQuizSvc, FlagQuizNoActiveQuizzesException


@inject('flag_quiz_end', [
    Dependency.get('flag_quiz_svc', FlagQuizSvc, InjectionType.SINGLE_BY_TYPE)
])
class FlagQuizEnd(FlagCmd):

    def __init__(self, flag_quiz_svc: FlagQuizSvc):
        self.flag_quiz_svc = flag_quiz_svc

    def is_applicable(self, ctx: CommandContext) -> bool:
        msg_lower = ctx.msg.content
        return end_quiz_pattern.search(msg_lower) is not None

    async def execute(self, ctx: CommandContext):
        try:
            quiz = self.flag_quiz_svc.get_quiz_by_ctx(ctx)
            self.flag_quiz_svc.end_quiz(ctx)
            leaderboard = self.get_leaderboard(quiz)
            await ctx.msg.channel.send(leaderboard)

        except FlagQuizNoActiveQuizzesException:
            await ctx.msg.channel.send('No active quizzes in this channel!')

    def get_leaderboard(self, quiz):
        winners = sorted(quiz.user_scores.items(), key=lambda user_score: user_score[1], reverse=True)
        if len(winners) == 0:
            return 'There were no correct answers \u2013 and therefore no winners.'

        leaderboard = 'Leaderboard:\n'
        for i, (user, score) in enumerate(winners):
            leaderboard += f'{i + 1}. {user.mention} ({score})\n'

        return leaderboard
