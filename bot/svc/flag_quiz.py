import asyncio
import random
import re
from enum import Enum

import discord
from discord import Member, User, File

from bot import ROOT_PATH
from bot.constants import country_code2country_name, country_codes, default_time_between_questions, \
    flag_quiz_replace_pattern
from bot.di.dependency_injector import inject
from bot.models import BaseSvc, CommandContext
from bot.utils import first


class FlagQuizInProgressException(Exception):
    pass


class FlagQuizNoActiveQuizzesException(Exception):
    pass


class FlagQuizNoActiveQuestionsException(Exception):
    pass


class FlagQuizStatus(Enum):
    STARTED = 0,
    ANSWERED = 1,
    WAITING_FOR_ANSWER = 2,
    PAUSED = 3,
    SKIPPED = 4


class FlagQuizQuestion:
    def __init__(self,
                 number: int,
                 country_code: str,
                 answer: list[str],
                 flag_image: File,
                 question_text: str = 'What country does this flag represent?'):
        self.number = number
        self.country_code = country_code
        self.answer = answer
        self.full_answer = answer[0]
        self.normalized_answers = [self.normalize_flag_quiz_answer(ans) for ans in answer]
        self.flag_image = flag_image
        self.question_text = question_text

    def is_answer(self, attempt: str):
        return self.normalize_flag_quiz_answer(attempt) in self.normalized_answers

    @staticmethod
    def normalize_flag_quiz_answer(answer: str):
        return re.sub(flag_quiz_replace_pattern, '', answer.lower())


class FlagQuizData:
    def __init__(self, guild_id: int, channel_id: int, status: FlagQuizStatus):
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.status = status

        self.question: FlagQuizQuestion | None = None
        self.user_scores = dict()

    def belongs_to(self, guild_id: int, channel_id: int):
        return self.guild_id == guild_id and self.channel_id == channel_id

    def try_answer(self, attempt: str, author: User | Member):
        if self.can_answer() and self.question.is_answer(attempt):
            self.increment_score(author)
            self.status = FlagQuizStatus.ANSWERED
            return True

        return False

    def skip(self):
        if self.status == FlagQuizStatus.SKIPPED:
            raise FlagQuizNoActiveQuestionsException()

        self.status = FlagQuizStatus.SKIPPED

    def increment_score(self, user: User | Member):
        score = self.user_scores.get(user)
        self.user_scores[user] = 1 + (0 if score is None else score)

    def can_answer(self):
        return self.status == FlagQuizStatus.WAITING_FOR_ANSWER


@inject(name='flag_quiz_svc')
class FlagQuizSvc(BaseSvc):

    def __init__(self):
        self.time_between_questions: float = default_time_between_questions
        self.quizzes: list[FlagQuizData] = []

    def get_quiz(self, guild_id: int, channel_id: int) -> FlagQuizData | None:
        return first(lambda q: q.belongs_to(guild_id, channel_id), self.quizzes)

    def get_quiz_by_ctx(self, ctx: CommandContext) -> FlagQuizData | None:
        return self.get_quiz(*self.get_quiz_params(ctx))

    def quiz_in_progress(self, ctx: CommandContext) -> bool:
        return self.get_quiz_by_ctx(ctx) is not None

    def start_new_quiz(self, ctx: CommandContext):
        self.validate_can_start_quiz(ctx)

        guild, channel = self.get_quiz_params(ctx)
        new_quiz = FlagQuizData(guild, channel, FlagQuizStatus.STARTED)
        self.quizzes.append(new_quiz)

    def end_quiz(self, ctx: CommandContext):
        currently_active_quiz = self.get_quiz_by_ctx(ctx)

        if currently_active_quiz is None:
            raise FlagQuizNoActiveQuizzesException()

        self.quizzes.remove(currently_active_quiz)

    def get_next_question(self, ctx: CommandContext):
        question = self.get_new_random_question(ctx)
        self.update_quiz_data_with_new_question(ctx, question)

        return question.question_text, question.flag_image

    def update_quiz_data_with_new_question(self, ctx, question):
        quiz = self.get_quiz_by_ctx(ctx)
        quiz.question = question

    async def pause_quiz(self, ctx: CommandContext):
        self.get_quiz_by_ctx(ctx).status = FlagQuizStatus.PAUSED
        await asyncio.sleep(self.time_between_questions)
        self.get_quiz_by_ctx(ctx).status = FlagQuizStatus.WAITING_FOR_ANSWER

    def try_answer(self, ctx: CommandContext):
        attempt = ctx.msg.content
        author = ctx.msg.author
        quiz = self.get_quiz_by_ctx(ctx)

        return quiz.try_answer(attempt, author)

    def reveal_answer(self, ctx: CommandContext):
        quiz = self.get_quiz_by_ctx(ctx)
        if quiz is None:
            raise FlagQuizNoActiveQuizzesException()

        quiz.skip()
        return quiz.question.full_answer

    def get_new_random_question(self, ctx: CommandContext) -> FlagQuizQuestion:
        current_question_number = self.get_current_question_number(ctx)
        new_country_code: str = random.choice(country_codes)
        new_country_name = country_code2country_name[new_country_code]

        return FlagQuizQuestion(
            current_question_number + 1,
            new_country_code,
            new_country_name,
            self.get_flag_image(new_country_code),
        )

    def get_current_question_number(self, ctx):
        quiz = self.get_quiz_by_ctx(ctx)
        if quiz and quiz.question and quiz.question.number is not None:
            return quiz.question.number
        return 0

    def validate_can_start_quiz(self, ctx: CommandContext):
        if self.quiz_in_progress(ctx):
            raise FlagQuizInProgressException

    def get_flag_image(self, country_code) -> File:
        return discord.File(f'{ROOT_PATH}/flags/{country_code}.png')

    def get_quiz_params(self, ctx: CommandContext):
        guild_id = ctx.msg.guild.id
        channel_id = ctx.msg.channel.id
        return guild_id, channel_id

    def get_question_num(self, ctx):
        return self.get_quiz_by_ctx(ctx).question.number
