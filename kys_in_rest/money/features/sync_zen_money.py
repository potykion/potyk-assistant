from kys_in_rest.config.features.load_config import LoadConfig


class SyncZenMoney:


    def __init__(self, load_config: LoadConfig):
        self.load_config = load_config

    def do(self):
        config = self.load_config.do()


        