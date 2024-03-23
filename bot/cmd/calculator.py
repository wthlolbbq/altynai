from typing import Any

from discord import Message, User  # NOQA

from bot.constants import calc_pattern, supported_operations, last_calc_answer_pattern
from bot.di.dependency_injector import inject, Dependency
from bot.di.models import InjectionType
from bot.models import CommandContext, BaseCmd
from bot.svc.session import SessionSvc
from bot.utils import matches


@inject('calculator', [
    Dependency.get('session_svc', SessionSvc, InjectionType.SINGLE_BY_TYPE)
])
class Calculator(BaseCmd):

    def __init__(self, session_svc: SessionSvc):
        self.session_svc = session_svc

    def is_applicable(self, ctx: CommandContext) -> bool:
        msg_lower = ctx.msg.content.lower()
        return matches(msg_lower, calc_pattern)

    async def execute(self, ctx: CommandContext):
        try:
            result = self.calculate(ctx)
            self.store_success_calc_result(ctx, result)
            await ctx.msg.channel.send(str(result))
        except (ArithmeticError, ValueError):
            await ctx.msg.channel.send('bruh')

    def calculate(self, ctx: CommandContext):
        num1, num2, op = self.get_calc_params(ctx)
        result = op(num1, num2)
        return self.round_if_needed(result)

    def store_success_calc_result(self, ctx: CommandContext, result: float | int):
        user_ans_storage = self.session_svc.last_calc_ans
        user_id = ctx.msg.author.id
        user_ans_storage[user_id] = result

    def get_calc_params(self, ctx: CommandContext) -> (float, float, Any):
        first, second, op = self.extract_raw_params(ctx.msg)

        num1 = self.to_num(ctx, first)
        num2 = self.to_num(ctx, second)
        operation = supported_operations[op].op

        return num1, num2, operation

    def to_num(self, ctx: CommandContext, user_input: str) -> float:
        if self.should_fetch_last_ans(user_input):
            return self.get_last_ans(ctx.msg.author.id)

        return float(user_input)

    def should_fetch_last_ans(self, user_input):
        return user_input.lower() == last_calc_answer_pattern

    def get_last_ans(self, user_id: int):
        try:
            return self.session_svc.last_calc_ans[user_id]
        except KeyError:
            raise ValueError()

    def extract_raw_params(self, msg: Message) -> (str, str, str):
        re_match = calc_pattern.search(msg.content)
        return re_match['first'], re_match['second'], re_match['op']

    @staticmethod
    def round_if_needed(result):
        if Calculator.is_number_integer(result):
            return int(result)
        else:
            return result

    @staticmethod
    def is_number_integer(num):
        return num % 1 == 0
