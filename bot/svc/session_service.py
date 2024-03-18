from bot.di.dependency_injector import inject
from bot.models import BaseSvc


@inject(name='session_svc', dependencies=[])
class SessionSvc(BaseSvc):
    def __init__(self):
        self.is_stuttering = False
        self.last_calc_ans = dict()
