from rabbit_helper import Rabbit


class AtSomeoneRabbit(Rabbit):
    EXCHANGE = "GUILD_STATE"

    def __init__(self, config):
        super(AtSomeoneRabbit, self).__init__(config["rabbit_uri"])

    async def parse_at_someone_0(self, data):
        print(data)
