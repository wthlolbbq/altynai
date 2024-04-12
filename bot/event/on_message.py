from discord import Client, Message  # NOQA

from bot.di.dependency_injector import inject, get_injected_by_class
from bot.models import BaseEvent, CommandContext, BaseCmd


@inject('on_message')
class OnMessageHandler(BaseEvent):

    async def handle(self, msg: Message, client: Client):
        if not self.is_bot_message(client, msg):
            ctx = CommandContext(msg, client)
            await self.send_response(ctx)

    def is_bot_message(self, client: Client, msg: Message):
        return msg.author == client.user

    async def send_response(self, ctx: CommandContext) -> None:
        try:
            await self.get_applicable_cmd_strategy(ctx).execute(ctx)
        except StopIteration:
            # No applicable strategies have been found.
            pass
        except Exception as e:
            print(e)

    def get_applicable_cmd_strategy(self, ctx: CommandContext) -> BaseCmd:
        cmd_strategies: list[BaseCmd] = get_injected_by_class(BaseCmd)
        prioritized_strategies = sorted(cmd_strategies, key=lambda cmd: cmd.get_priority())
        applicable_cmd_strategies = (i for i in prioritized_strategies if i.is_applicable(ctx))
        return next(applicable_cmd_strategies)
