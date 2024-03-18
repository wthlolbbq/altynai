import os

from bot.di.constants import user_module_suffix, reserved_module_prefix


def get_sibling_user_modules(file_path) -> list[str]:
    file_dir = os.path.dirname(file_path)
    sibling_files = os.listdir(file_dir)
    return [f.removesuffix(user_module_suffix) for f in sibling_files if is_user_module(f)]


def is_user_module(filename: str) -> bool:
    return filename.endswith(user_module_suffix) and not filename.startswith(reserved_module_prefix)
