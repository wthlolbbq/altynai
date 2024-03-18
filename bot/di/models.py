from enum import Enum


class CircularDependencyException(Exception):
    pass


class InjectionType(Enum):
    BY_NAME = 1,
    BY_TYPE = 2,


class Dependency:
    def __init__(self, name, clazz, injection_method: InjectionType):
        self.name = name
        self.clazz = clazz
        self.injection_method = injection_method
