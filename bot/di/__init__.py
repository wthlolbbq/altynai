from bot.cmd import *  # NOQA
from bot.di.dependency_injector import inject_dependencies
from bot.event import *  # NOQA
from bot.svc import *  # NOQA

inject_dependencies()

"""
In order to use Dependency Injection (DI) follow these steps (skip to 
step 4 if a package that supports DI already exists).

1. Create a package which is going to contain only injection classes.
2. Create an __init__.py file in the created package, containing the following:

from bot.di.utils import get_sibling_user_modules
__all__ = get_sibling_user_modules(__file__)
# This package should only contain dependency injection classes.

3. Import everything from that package at the beginning of this file, e.g.:

from bot.my.package import *  # NOQA

4. Add the `inject` decorator to your injection classes, and optionally add 
dependencies, e.g.

@inject('my_injection', [
    Dependency.get('some_svc', SomeSvc, InjectionType.BY_NAME)
])
class MyInjection:
    ...

"""
