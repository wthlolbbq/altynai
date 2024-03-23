from discord import Client, Message  # NOQA


class AppState:
    def __init__(self, is_stuttering: bool, last_calc_ans: dict):
        self.is_stuttering = is_stuttering
        self.last_calc_ans = last_calc_ans


class CommandContext:
    def __init__(self, msg: Message, client: Client):
        self.msg = msg
        self.client = client


class BaseCmd:
    def is_applicable(self, ctx: CommandContext) -> bool:
        raise NotImplementedError()

    async def execute(self, ctx: CommandContext):
        raise NotImplementedError()


class BaseSvc:
    pass


class BaseEvent:
    pass


class CalculationOperation:
    def __init__(self, re_pattern: str, op):
        self.re_pattern = re_pattern
        self.op = op
