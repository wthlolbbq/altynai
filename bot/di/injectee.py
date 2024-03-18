from typing import Any

from bot.di.models import Dependency, InjectionType


class Injectee:
    def __init__(self, name, clazz, dependencies: list[Dependency]):
        self.name = name
        self.clazz = clazz
        self.dependencies = dependencies

    # TODO Optimize, refactor iteration into a method and reuse.
    def has_resolved_dependencies(self, resolved_deps: dict['Injectee', Any]) -> bool:
        unresolved_count = len(self.dependencies)
        for unresolved_dep in self.dependencies:
            for resolved_dep in resolved_deps.items():
                if Injectee.deps_match(unresolved_dep, *resolved_dep):
                    unresolved_count -= 1

        return unresolved_count == 0

    def construct(self, resolved_deps: dict['Injectee', Any]):
        constructor_params = {}
        for unresolved_dep in self.dependencies:
            for injectee, instance in resolved_deps.items():
                if Injectee.deps_match(unresolved_dep, injectee, instance):
                    constructor_params[unresolved_dep.name] = instance

        return self.clazz(**constructor_params)

    @staticmethod
    def deps_match(unresolved_dep: Dependency, injectee, instance):
        has_matching_class = isinstance(instance, unresolved_dep.clazz)
        has_matching_name = (unresolved_dep.injection_method != InjectionType.BY_NAME
                             or unresolved_dep.name == injectee.name)
        return has_matching_class and has_matching_name
