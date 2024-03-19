from bot.constants import send_msg_to_channel_pattern
from bot.di.dependency_injector import inject
from bot.models import CommandContext, BaseCmd
from bot.utils import get_channel_by_name, matches


@inject('ch_msg_sender')
class ChannelMessageSender(BaseCmd):
    def is_applicable(self, ctx: CommandContext) -> bool:
        msg_content = ctx.msg.content
        return matches(msg_content, send_msg_to_channel_pattern)

    async def execute(self, ctx: CommandContext):
        channel, msg_to_send = self.get_channel_and_msg(ctx)
        if channel:
            await channel.send(msg_to_send)
        else:
            raise Exception('No channel found for the given name ' + ctx.msg.content)

    def get_channel_and_msg(self, ctx: CommandContext):
        channel_name, user_msg = self.get_raw_channel_msg_params(ctx)
        channel = get_channel_by_name(ctx.client, channel_name)
        return channel, user_msg

    @staticmethod
    def get_raw_channel_msg_params(ctx: CommandContext):
        msg_content = ctx.msg.content
        re_match = send_msg_to_channel_pattern.search(msg_content)
        return re_match['channel_name'], re_match['user_message']
