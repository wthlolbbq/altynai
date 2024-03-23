from enum import Enum


class CircularDependencyException(Exception):
    pass


class InjectionType(Enum):
    SINGLE_BY_NAME = 1,
    SINGLE_BY_TYPE = 2,
    ALL_BY_TYPE = 3,
