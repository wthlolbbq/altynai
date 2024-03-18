from discord import Message  # NOQA

from bot.constants import calc_re, supported_operations
from bot.di.dependency_injector import inject
from bot.di.models import Dependency, InjectionType
from bot.models import CommandContext, BaseCmd
from bot.svc.session_service import SessionSvc


@inject('calculator', [
    Dependency('session_svc', SessionSvc, InjectionType.BY_NAME)
])
class Calculator(BaseCmd):

    def __init__(self, session_svc: SessionSvc):
        self.session_svc = session_svc

    def is_applicable(self, ctx: CommandContext) -> bool:
        msg_lower = ctx.msg.content.lower()
        return calc_re.search(msg_lower) is not None

    async def execute(self, ctx: CommandContext):
        calc_operands = Calculator.extract_calc_params(ctx.msg)
        last_user_ans = self.session_svc.last_calc_ans
        user_id = ctx.msg.author.id

        result = self.calculate(ctx, **calc_operands)
        if result is None:
            await ctx.msg.channel.send('bruh')
        else:
            last_user_ans[user_id] = result
            await ctx.msg.channel.send(str(result))

    def calculate(self, ctx: CommandContext, first: str, second: str, op: str) -> float | int | None:
        try:
            num1 = self.to_num(ctx, first)
            num2 = self.to_num(ctx, second)
            operation = supported_operations[op]

            return Calculator.round(operation(num1, num2))
        except (ArithmeticError, ValueError):
            return None

    def to_num(self, ctx: CommandContext, user_input: str):
        user_id = ctx.msg.author.id
        last_user_ans = self.session_svc.last_calc_ans

        if user_input.lower() != 'ans':
            return float(user_input)
        elif (last_ans := last_user_ans.get(user_id, None)) is not None:
            return last_ans
        else:
            raise ValueError()

    @staticmethod
    def extract_calc_params(msg: Message):
        return calc_re.search(msg.content).groupdict()

    @staticmethod
    def round(result):
        is_int = result % 1 == 0
        return int(result) if is_int else result
