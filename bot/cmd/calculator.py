from discord import Message, User  # NOQA

from bot.const.constants import calc_pattern
from bot.di.dependency_injector import inject, Dependency
from bot.di.models import InjectionType
from bot.models import CommandContext, BaseCmd, LastCalcResultDoesNotExistException, CalculatorProcessResult
from bot.process.calculator_process import CalculatorProcess
from bot.svc.session import SessionSvc
from bot.utils import matches


@inject('calculator', [
    Dependency.get('session_svc', SessionSvc, InjectionType.SINGLE_BY_TYPE),
    Dependency.get('calculator_process', CalculatorProcess, InjectionType.SINGLE_BY_TYPE)
])
class Calculator(BaseCmd):

    def __init__(self, session_svc: SessionSvc, calculator_process: CalculatorProcess):
        self.calculator_process: CalculatorProcess = calculator_process
        self.session_svc = session_svc

    def is_applicable(self, ctx: CommandContext) -> bool:
        msg_lower = ctx.msg.content.lower()
        return matches(msg_lower, calc_pattern)

    async def execute(self, ctx: CommandContext):
        try:
            result: CalculatorProcessResult = self.calculator_process.execute_with_hooks(ctx)
            await ctx.msg.channel.send(result.formatted_result)
        except (ArithmeticError, LastCalcResultDoesNotExistException):
            await ctx.msg.channel.send('bruh')
