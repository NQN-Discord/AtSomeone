from typing import Optional
from rabbit_helper import Rabbit
from aiohttp import ClientSession
import random
from discord import Webhook, AsyncWebhookAdapter, AllowedMentions

responses = [
    r"(╯°□°）╯︵ ┻━┻",
    r"ಠ_ಠ",
    r"(◕‿◕✿)",
    r"✿ ͡◕ ᴗ◕)つ━━✫・o",
    r"¯\_(ツ)_/¯",
    r"(⁄ ⁄•⁄ω⁄•⁄ ⁄)",
    r"ヽ༼ ಠ益ಠ ༽ﾉ",
    r"༼ つ ◕_◕ ༽つ",
    r"¯(°_o)/¯",
    r"(∩ ͡° ͜ʖ ͡°)⊃━✿✿✿✿✿✿",
    r"(∩ ͡° ͜ʖ ͡°)⊃━☆ﾟ. o ･ ｡ﾟ",
    r"ノ┬─┬ノ ︵ ( \o°o)\ ",
]


class AtSomeoneRabbit(Rabbit):
    def __init__(self, config, cur):
        super(AtSomeoneRabbit, self).__init__(config["rabbit_uri"])
        self.webhook_uri = config["webhook_uri"]
        self.cur = cur

    async def parse_at_someone_0(self, data):
        guild_id = data["guild_id"]
        channel_id = data["channel_id"]
        webhook_url = await self.get_webhook(guild_id, channel_id)
        if webhook_url is None:
            return

        async with ClientSession() as client:
            webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(client))
            user_id = await self.get_random_user(guild_id)
            author = data["author"]
            avatar = author["avatar"]
            if avatar:
                avatar = f"https://cdn.discordapp.com/avatars/{author['user_id']}/{avatar}.png?size=256"
            else:
                avatar = f"https://cdn.discordapp.com/embed/avatars/{int(author['discriminator']) % 5}.png"

            await webhook.send(
                content=f"**@someone {random.choice(responses)} (<@{user_id}>)**",
                username=data["nickname"] or author["username"],
                avatar_url=avatar,
                allowed_mentions=AllowedMentions(users=False)
            )

    async def get_webhook(self, guild_id: str, channel_id: str) -> Optional[str]:
        async with ClientSession() as client:
            async with client.get(f"{self.webhook_uri}/webhooks/{guild_id}/{channel_id}") as resp:
                webhooks = (await resp.json())["webhooks"]
                if not webhooks:
                    return
                webhook_uri = webhooks[0]
                return webhook_uri

    async def get_random_user(self, guild_id: str) -> str:
        await self.cur.execute(
            "SELECT user_id FROM members WHERE guild_id = %(guild_id)s ORDER BY user_id DESC LIMIT 200",
            parameters={
                "guild_id": guild_id
            }
        )
        user_ids = (await self.cur.fetchall())
        return random.choice(user_ids)[0]
