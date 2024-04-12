from bot.di.dependency_injector import inject, Dependency
from bot.di.models import InjectionType
from bot.models import CmdProcess, CalculatorProcessExecutor, CalculatorProcessResult
from bot.process.calculator_process_hooks import CalculatorPostProcessingHook


@inject('calculator_process', [
    Dependency.get('executor', CalculatorProcessExecutor, InjectionType.SINGLE_BY_TYPE),
    Dependency.get('post_processing_hooks', CalculatorPostProcessingHook, InjectionType.ALL_BY_TYPE),
])
class CalculatorProcess(CmdProcess):
    pass
