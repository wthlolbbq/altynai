from re import Pattern
from typing import Iterable

import discord  # NOQA
from discord import Client, File  # NOQA

from bot import ROOT_PATH


def get_channel_by_name(client: Client, ch_name: str):
    all_channels = client.get_all_channels()
    return discord.utils.get(all_channels, name=ch_name)


def empty_if_none(arg: list | None) -> list:
    return [] if arg is None else arg


def matches(s: str, pattern: Pattern[str]):
    return pattern.search(s) is not None


def first(filter_function, iterable: Iterable):
    return next(filter(filter_function, iterable), None)


def is_number_integer(num: float | int):
    return num % 1 == 0


def get_flag_image(country_code) -> File:
    return discord.File(f'{ROOT_PATH}/flags/{country_code}.png')
