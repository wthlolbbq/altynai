from typing import Any

from bot.di.injectee import Injectee
from bot.di.models import CircularDependencyException, Dependency
from bot.utils import empty_if_none

resolved_injections: dict[Injectee, Any] = dict()
pending_injections: list[Injectee] = []


def get_injected_by_class(cls):
    return [i for i in resolved_injections.values() if isinstance(i, cls)]


def get_injected_by_name(name: str) -> Any | None:
    for (injectee, instance) in resolved_injections.items():
        if injectee.name == name:
            return instance

    return None


def inject(name: str, dependencies: list[Dependency] = None):
    """Decorator for injectables."""

    def decorator_wrapper(cls):
        injectee = Injectee(name, cls, empty_if_none(dependencies))
        if injectee.has_resolved_dependencies(resolved_injections):
            resolved_injections[injectee] = injectee.construct(resolved_injections)
        else:
            pending_injections.append(injectee)

        return cls

    return decorator_wrapper


def inject_dependencies():
    while True:
        len_pre_prune = len(pending_injections)
        for injectee in pending_injections[:]:
            if injectee.has_resolved_dependencies(resolved_injections):
                resolved_injections[injectee] = injectee.construct(resolved_injections)
                pending_injections.remove(injectee)

        len_post_prune = len(pending_injections)
        if len_post_prune == 0:
            return
        if len_pre_prune == len_post_prune:
            raise CircularDependencyException()
