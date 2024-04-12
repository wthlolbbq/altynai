from discord import Client, Message  # NOQA

from bot.helper.ordered import DEFAULT_PRIORITY, Ordered, HIGHEST_PRIORITY
from bot.utils import empty_if_none


class AppState:
    def __init__(self, is_stuttering: bool, last_calc_ans: dict):
        self.is_stuttering = is_stuttering
        self.last_calc_ans = last_calc_ans


class CommandContext:
    def __init__(self, msg: Message, client: Client):
        self.msg = msg
        self.client = client


class BaseCmd(Ordered):
    def is_applicable(self, ctx: CommandContext) -> bool:
        raise NotImplementedError()

    async def execute(self, ctx: CommandContext):
        raise NotImplementedError()

    def get_priority(self):
        return DEFAULT_PRIORITY


class FlagCmd(BaseCmd):
    def get_priority(self):
        return HIGHEST_PRIORITY


class BaseSvc:
    pass


class BaseEvent:
    pass


class CalculationOperation:
    def __init__(self, re_pattern: str, op):
        self.re_pattern = re_pattern
        self.op = op


class PreProcessingHook:
    def run(self, ctx: CommandContext):
        raise NotImplementedError()


class PostProcessingHook:
    def run(self, ctx: CommandContext, result):
        raise NotImplementedError()


class ProcessingExecutor:
    def get_result(self, ctx: CommandContext):
        raise NotImplementedError()


class CmdProcess:

    def __init__(
            self,
            executor: ProcessingExecutor,
            pre_processing_hooks: list[PreProcessingHook] = None,
            post_processing_hooks: list[PostProcessingHook] = None,
    ):
        self.executor = executor
        self.post_processing_hooks = empty_if_none(post_processing_hooks)
        self.pre_processing_hooks = empty_if_none(pre_processing_hooks)

    def execute_with_hooks(self, ctx: CommandContext):
        for hook in self.pre_processing_hooks:
            hook.run(ctx)

        result = self.executor.get_result(ctx)

        for hook in self.post_processing_hooks:
            hook.run(ctx, result)

        return result


class CalculatorProcessResult:
    def __init__(self, raw_result: int | float, formatted_result: str):
        self.formatted_result = formatted_result
        self.raw_result = raw_result


class CalculatorProcessExecutor(ProcessingExecutor):
    pass


class CalculatorPostProcessingHook(PostProcessingHook):
    pass


class LastCalcResultDoesNotExistException(Exception):
    pass
