from typing import Any

from discord import Message  # NOQA

from bot.const.constants import supported_operations, last_calc_answer_pattern, calc_pattern
from bot.di.dependency_injector import Dependency, inject
from bot.di.models import InjectionType
from bot.models import CommandContext, CalculatorProcessExecutor, LastCalcResultDoesNotExistException, \
    CalculatorProcessResult
from bot.svc.session import SessionSvc
from bot.utils import is_number_integer


@inject('calculator_process_executor', [
    Dependency.get('session_svc', SessionSvc, InjectionType.SINGLE_BY_TYPE)
])
class CalculatorProcessExecutorImpl(CalculatorProcessExecutor):

    def __init__(self, session_svc: SessionSvc):
        self.session_svc = session_svc

    def get_result(self, ctx: CommandContext):
        raw_result = self.calculate(ctx)
        result_msg = str(raw_result)

        return CalculatorProcessResult(raw_result, result_msg)

    def calculate(self, ctx: CommandContext):
        num1, num2, op = self.get_calc_params(ctx)
        result = op(num1, num2)
        return self.round_if_needed(result)

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
            raise LastCalcResultDoesNotExistException()

    def extract_raw_params(self, msg: Message) -> (str, str, str):
        re_match = calc_pattern.search(msg.content)
        return re_match['first'], re_match['second'], re_match['op']

    def round_if_needed(self, result):
        if is_number_integer(result):
            return int(result)
        else:
            return result
