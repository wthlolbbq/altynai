import asyncio
import random
import re
from enum import Enum
from typing import Type

from discord import Member, User, File  # NOQA

from bot.const.constants import country_code2country_name, default_time_between_questions, \
    start_quiz_pattern, country_code2capital, country_code2population, non_alpha_pattern
from bot.di.dependency_injector import inject
from bot.models import BaseSvc, CommandContext
from bot.utils import first, get_flag_image

max_rel_deviation_from_correct_answer = 25  # Percentage.


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
                 answer: any,
                 flag_image: File,
                 question_text: str):
        self.number = number
        self.country_code = country_code
        self.answer = answer
        self.question_text = question_text
        self.flag_image = flag_image

    def get_full_answer(self):
        raise NotImplementedError()

    def is_answer(self, attempt: str):
        raise NotImplementedError()


class FlagCountryQuizQuestion(FlagQuizQuestion):

    def get_full_answer(self):
        return self.answer[0]

    def is_answer(self, attempt: str):
        normalized_answers = [self.normalize_answer(ans) for ans in self.answer]
        return self.normalize_answer(attempt) in normalized_answers

    def normalize_answer(self, answer: str):
        return re.sub(non_alpha_pattern, '', answer.lower())


class FlagCapitalQuizQuestion(FlagCountryQuizQuestion):
    pass


class FlagPopulationQuizQuestion(FlagQuizQuestion):

    def get_full_answer(self):
        return f'{self.answer:,}'

    def is_answer(self, attempt: str):
        normalized_answer = self.convert_to_number(attempt)
        if normalized_answer is None:
            return False

        return self.is_attempt_within_percent_of_correct(normalized_answer, max_rel_deviation_from_correct_answer)

    def is_attempt_within_percent_of_correct(self, normalized_answer, tolerance):
        abs_tolerance = tolerance / 100 * self.answer
        potential_answers = (
            normalized_answer,
            normalized_answer * 1_000,  # thousands
            normalized_answer * 1_000_000,  # millions
            normalized_answer * 1_000_000_000,  # billions
        )
        return any(abs(ans - self.answer) < abs_tolerance for ans in potential_answers)

    def convert_to_number(self, answer: str) -> float | None:
        try:
            return float(answer)
        except ValueError:
            return None


class FlagQuizData:
    def __init__(self, guild_id: int, channel_id: int, status: FlagQuizStatus):
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.status = status

        self.question: FlagQuizQuestion | None = None
        self.user_scores = dict()

    def get_current_question_number(self):
        return 0 if self.question is None else self.question.number

    def belongs_to(self, guild_id: int, channel_id: int):
        return self.guild_id == guild_id and self.channel_id == channel_id

    def try_answer(self, attempt: str, author: User | Member):
        if self.can_answer() and self.question.is_answer(attempt):
            self.increment_score(author)
            self.status = FlagQuizStatus.ANSWERED
            return True

        return False

    def skip_question(self):
        if self.status != FlagQuizStatus.WAITING_FOR_ANSWER:
            raise FlagQuizNoActiveQuestionsException()

        self.status = FlagQuizStatus.SKIPPED

    def increment_score(self, user: User | Member):
        score = self.user_scores.get(user)
        self.user_scores[user] = 1 + (0 if score is None else score)

    def can_answer(self):
        return self.status == FlagQuizStatus.WAITING_FOR_ANSWER

    def go_to_next_question(self) -> FlagQuizQuestion:
        self.question = self.generate_next_question()
        return self.question

    def generate_next_question(self) -> FlagQuizQuestion:
        raise NotImplementedError()


class FlagCountryQuizData(FlagQuizData):

    def generate_next_question(self) -> FlagQuizQuestion:
        country_code: str = random.choice(list(country_code2country_name.keys()))
        country_name = country_code2country_name[country_code]
        return FlagCountryQuizQuestion(
            self.get_current_question_number() + 1,
            country_code,
            country_name,
            get_flag_image(country_code),
            'What country does this flag represent?'
        )


class FlagCapitalQuizData(FlagQuizData):

    def generate_next_question(self) -> FlagQuizQuestion:
        country_code: str = random.choice(list(country_code2capital.keys()))
        capital = country_code2capital[country_code]
        return FlagCapitalQuizQuestion(
            self.get_current_question_number() + 1,
            country_code,
            capital,
            get_flag_image(country_code),
            'What is the capital of the country represented by this flag?'
        )


class FlagPopulationQuizData(FlagQuizData):

    def generate_next_question(self) -> FlagQuizQuestion:
        country_code: str = random.choice(list(country_code2population.keys()))
        population = country_code2population[country_code]
        return FlagPopulationQuizQuestion(
            self.get_current_question_number() + 1,
            country_code,
            population,
            get_flag_image(country_code),
            'What is the population of the country represented by this flag?'
        )


quiz_type_mapping: dict[str, Type[FlagCountryQuizData]] = {
    'country': FlagCountryQuizData,
    'flag': FlagCountryQuizData,
    'capital': FlagCapitalQuizData,
    'capitals': FlagCapitalQuizData,
    'pop': FlagPopulationQuizData,
    'population': FlagPopulationQuizData,
}


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

        new_quiz = self.get_new_quiz(ctx)
        self.quizzes.append(new_quiz)

    def end_quiz(self, ctx: CommandContext):
        self.validate_can_end_quiz(ctx)

        quiz = self.get_quiz_by_ctx(ctx)
        self.quizzes.remove(quiz)

    def get_new_quiz(self, ctx):
        guild, channel = self.get_quiz_params(ctx)
        quiz_type = self.get_quiz_type(ctx.msg.content)
        return quiz_type(guild, channel, FlagQuizStatus.STARTED)

    def get_next_question_data(self, ctx: CommandContext):
        question = self.get_quiz_by_ctx(ctx).go_to_next_question()
        print(question.answer)
        return question.question_text, question.flag_image

    async def pause_quiz(self, ctx: CommandContext):
        self.get_quiz_by_ctx(ctx).status = FlagQuizStatus.PAUSED
        await asyncio.sleep(self.time_between_questions)
        self.get_quiz_by_ctx(ctx).status = FlagQuizStatus.WAITING_FOR_ANSWER

    def try_answer(self, ctx: CommandContext):
        quiz = self.get_quiz_by_ctx(ctx)
        attempt = ctx.msg.content
        author = ctx.msg.author

        return quiz.try_answer(attempt, author)

    def reveal_answer(self, ctx: CommandContext):
        self.validate_can_reveal_answer(ctx)

        quiz = self.get_quiz_by_ctx(ctx)
        quiz.skip_question()
        return quiz.question.get_full_answer()

    def validate_can_start_quiz(self, ctx: CommandContext):
        if self.quiz_in_progress(ctx):
            raise FlagQuizInProgressException()

    def validate_can_reveal_answer(self, ctx):
        if not self.quiz_in_progress(ctx):
            raise FlagQuizNoActiveQuizzesException()

    def validate_can_end_quiz(self, ctx):
        if not self.quiz_in_progress(ctx):
            raise FlagQuizNoActiveQuizzesException()

    def get_quiz_params(self, ctx: CommandContext):
        guild_id = ctx.msg.guild.id
        channel_id = ctx.msg.channel.id
        return guild_id, channel_id

    def get_question_num(self, ctx):
        return self.get_quiz_by_ctx(ctx).question.number

    def get_quiz_type(self, msg_content: str) -> Type[FlagCountryQuizData]:
        quiz_type_raw = start_quiz_pattern.search(msg_content)['quiz_type']
        return quiz_type_mapping[quiz_type_raw]
