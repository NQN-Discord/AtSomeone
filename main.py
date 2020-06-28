import yaml
import asyncio
from rabbit_parsers import AtSomeoneRabbit
from aiopg import connect
import sentry_sdk


async def main(config):
    if config.get("sentry"):
        sentry_sdk.init(config["sentry"])
    async with connect(config["postgres_uri"]) as conn:
        async with conn.cursor() as cur:
            rabbit = AtSomeoneRabbit(config, cur)
            await rabbit.connect()
            print("Connected")
            await rabbit.consume()


if __name__ == "__main__":
    with open("config.yaml") as conf_file:
        config = yaml.load(conf_file, Loader=yaml.SafeLoader)

    asyncio.run(main(config))
