from bot.di.dependency_injector import Dependency, inject
from bot.di.models import InjectionType
from bot.models import CommandContext, CalculatorPostProcessingHook, CalculatorProcessResult
from bot.svc.session import SessionSvc


@inject('calculator_process_store_last_calc', [
    Dependency.get('session_svc', SessionSvc, InjectionType.SINGLE_BY_TYPE)
])
class CalculatorProcessStoreLastCalc(CalculatorPostProcessingHook):

    def __init__(self, session_svc: SessionSvc):
        self.session_svc = session_svc

    def run(self, ctx: CommandContext, result: CalculatorProcessResult):
        user_ans_storage = self.session_svc.last_calc_ans
        user_id = ctx.msg.author.id
        user_ans_storage[user_id] = result.raw_result
