import discord  # NOQA
from discord import Client  # NOQA


def get_channel_by_name(client: Client, ch_name: str):
    all_channels = client.get_all_channels()
    return discord.utils.get(all_channels, name=ch_name)
