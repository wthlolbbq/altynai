from typing import Any

from bot.di.models import CircularDependencyException
from bot.di.models import InjectionType
from bot.utils import empty_if_none
from bot.utils import first


class Injection:
    def __init__(self, name, cls, dependencies: list['Dependency'] | None):
        self.name = name
        self.cls = cls
        self.dependencies: list[Dependency] = empty_if_none(dependencies)

    def are_all_deps_resolved(self, di_registry: dict['Injection', Any], pending_di_registry: list) -> bool:
        resolved_deps = list(1 for dep in self.dependencies if dep.is_resolved(di_registry, pending_di_registry))
        return len(resolved_deps) == len(self.dependencies)

    def construct_instance(self, resolved_deps: dict['Injection', Any]):
        constructor_params = {
            dep.name: dep.get_matching_instance(resolved_deps) for dep in self.dependencies
        }
        return self.cls(**constructor_params)


class Dependency:

    def __init__(self, name):
        self.name = name

    def is_resolved(self, di_registry: dict[Injection, Any], pending_di_registry: list):
        raise NotImplementedError()

    def get_matching_instance(self, di_registry: dict[Injection, Any]):
        """Must be preceded by a call to `is_resolved`."""
        raise NotImplementedError()

    @staticmethod
    def get(name, cls, injection_method: InjectionType):
        if injection_method == InjectionType.SINGLE_BY_NAME:
            return DependencyByNameSingle(name)
        elif injection_method == InjectionType.SINGLE_BY_TYPE:
            return DependencyByTypeSingle(name, cls)
        elif injection_method == InjectionType.ALL_BY_TYPE:
            return DependencyByTypeAll(name, cls)
        else:
            raise NotImplementedError()


class DependencyByNameSingle(Dependency):
    def __init__(self, name):
        super().__init__(name)

    def is_resolved(self, di_registry: dict[Injection, Any], pending_di_registry: list):
        return first(lambda injection: injection.name == self.name, di_registry.keys()) is not None

    def get_matching_instance(self, di_registry: dict[Injection, Any]):
        for injection, instance in di_registry.items():
            if injection.name == self.name:
                return instance


class DependencyByTypeSingle(Dependency):
    def __init__(self, name, cls):
        super().__init__(name)
        self.cls = cls

    def is_resolved(self, di_registry: dict[Injection, Any], pending_di_registry: list):
        return first(lambda injection: isinstance(injection, self.cls), di_registry.values()) is not None

    def get_matching_instance(self, di_registry: dict[Injection, Any]):
        return first(lambda instance: isinstance(instance, self.cls), di_registry.values())


class DependencyByTypeAll(Dependency):
    def __init__(self, name, cls):
        super().__init__(name)
        self.cls = cls

    def is_resolved(self, di_registry: dict[Injection, Any], pending_di_registry: list):
        return first(lambda injection: issubclass(injection.cls, self.cls), pending_di_registry) is None

    def get_matching_instance(self, di_registry: dict[Injection, Any]):
        return list(filter(lambda instance: isinstance(instance, self.cls), di_registry.values()))


_di_registry: dict[Injection, Any] = dict()
_pending_di_registry: list[Injection] = []


def get_injected_by_class(cls) -> list:
    # TODO optimize with a cache
    return [i for i in _di_registry.values() if isinstance(i, cls)]


def get_injected_by_name(name: str) -> Any | None:
    # TODO optimize with a cache
    for (injection, instance) in _di_registry.items():
        if injection.name == name:
            return instance

    return None


def inject(name: str, dependencies: list[Dependency] = None):
    """Decorator for injections."""

    def decorator_wrapper(cls):
        injection = Injection(name, cls, dependencies)
        _pending_di_registry.append(injection)
        return cls

    return decorator_wrapper


def inject_dependencies():
    while True:
        pre_prune_size = len(_pending_di_registry)
        for injection in _pending_di_registry[:]:
            if injection.are_all_deps_resolved(_di_registry, _pending_di_registry):
                _di_registry[injection] = injection.construct_instance(_di_registry)
                _pending_di_registry.remove(injection)

        post_prune_size = len(_pending_di_registry)
        if post_prune_size == 0:
            return
        if pre_prune_size == post_prune_size:
            raise CircularDependencyException()
