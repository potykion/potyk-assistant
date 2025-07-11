import time

import requests


class ZenMoneyClient:
    """
    https://github.com/zenmoney/ZenPlugins/wiki/ZenMoney-API
    """

    def __init__(self, zen_money_token):
        self.zen_money_token = zen_money_token

    def diff(self, current_client_timestamp=None, server_timestamp=0):
        current_client_timestamp = current_client_timestamp or int(time.time())
        resp = requests.post(
            "https://api.zenmoney.ru/v8/diff/",
            json={
                "currentClientTimestamp": current_client_timestamp,
                "server_timestamp": server_timestamp,
            },
            headers={
                "Authorization": f"Bearer {self.zen_money_token}",
            },
        )
        resp.raise_for_status()
        resp_json = resp.json()
        return resp_json
