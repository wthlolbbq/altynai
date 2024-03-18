from bot.constants import send_msg_to_channel_re
from bot.di.dependency_injector import inject
from bot.models import CommandContext, BaseCmd
from bot.utils import get_channel_by_name


@inject('ch_msg_sender', [])
class ChannelMessageSender(BaseCmd):
    def is_applicable(self, ctx: CommandContext) -> bool:
        msg_content = ctx.msg.content
        return send_msg_to_channel_re.search(msg_content) is not None

    async def execute(self, ctx: CommandContext):
        channel, msg_to_send = ChannelMessageSender.get_channel_and_msg(ctx)
        if channel:
            await channel.send(msg_to_send)
        else:
            raise Exception('No channel found for the given name ' + ctx.msg.content)

    @staticmethod
    def get_channel_and_msg(ctx: CommandContext):
        msg_content = ctx.msg.content
        re_match = send_msg_to_channel_re.search(msg_content)
        channel = get_channel_by_name(ctx.client, re_match['channel_name'])
        return channel, re_match['user_message']
