import yaml
import asyncio
from rabbit_parsers import AtSomeoneRabbit


async def main(config):
    rabbit = AtSomeoneRabbit(config)
    await rabbit.connect()
    print("Connected")
    await rabbit.consume()


if __name__ == "__main__":
    with open("config.yaml") as conf_file:
        config = yaml.load(conf_file, Loader=yaml.SafeLoader)

    asyncio.run(main(config))
