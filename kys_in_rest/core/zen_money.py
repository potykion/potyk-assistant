import time
from typing import TypedDict

import requests

# region zen money models


class ZenMoneyInstrument(TypedDict, total=False):
    """
     {
        "id": 2,
        "title": "Российский рубль",
        "shortTitle": "RUB",
        "symbol": "руб.",
        "rate": 1,
        "changed": 1752367497
    }
    """

    id: int
    title: str
    shortTitle: str
    symbol: str
    rate: int
    changed: int


class ZenMoneyCountry(TypedDict, total=False):
    """
    {
         "id": 1,
         "title": "Россия",
         "currency": 2,
         "domain": "ru"
     }
    """

    id: int
    title: str
    currency: str
    domain: str


class ZenMoneyCompany(TypedDict, total=False):
    """
    {
        "id": 3,
        "title": "Альфа-Банк",
        "www": "alfabank.ru",
        "country": 1,
        "fullTitle": null,
        "changed": 1371739196,
        "deleted": false,
        "countryCode": "RU"
    }
    """

    id: int
    title: str
    www: str
    country: int
    fullTitle: str | None
    changed: int
    deleted: bool
    countryCode: str


class ZenMoneyUser(TypedDict, total=False):
    """
    {
          "id": 686527,
          "country": 1,
          "login": null,
          "parent": null,
          "countryCode": "RU",
          "email": "potykion@gmail.com",
          "changed": 1718692559,
          "currency": 2,
          "paidTill": 4713504186,
          "monthStartDay": 1,
          "isForecastEnabled": true,
          "planBalanceMode": "excludeOpeningBalance",
          "planSettings": "[]",
          "subscription": "10yearssubscriptionr",
          "subscriptionRenewalDate": null
      }
    """

    id: int
    country: int
    login: str | None
    parent: str | None
    countryCode: str
    email: str
    countryCode: str
    currency: int
    paidTill: int
    monthStartDay: int
    isForecastEnabled: bool
    planBalanceMode: str
    planSettings: str
    subscription: str
    subscriptionRenewalDate: str | None


class ZenMoneyAccount(TypedDict, total=False):
    """{
        "id": "7a861d50-a037-4ba7-badc-c7433f70c3f5",
        "user": 686527,
        "instrument": 2,
        "type": "checking",
        "role": null,
        "private": false,
        "savings": false,
        "title": "Ozon",
        "inBalance": false,
        "creditLimit": 0,
        "startBalance": 420.14,
        "balance": 126.17,
        "company": 15685,
        "archive": false,
        "enableCorrection": true,
        "balanceCorrectionType": "request",
        "startDate": null,
        "capitalization": null,
        "percent": null,
        "changed": 1751981774,
        "syncID": [
            "0484"
        ],
        "enableSMS": false,
        "endDateOffset": null,
        "endDateOffsetInterval": null,
        "payoffStep": null,
        "payoffInterval": null
    },"""

    id: int
    user: int
    instrument: int
    type: str
    role: str | None
    private: bool
    savings: bool
    title: str
    inBalance: bool
    creditLimit: int
    startBalance: int
    balance: int
    company: int
    archive: bool
    enableCorrection: bool
    balanceCorrectionType: str
    startDate: str | None
    capitalization: str | None
    percent: float | None
    changed: int
    syncID: list[int]
    enableSMS: bool
    endDateOffset: int | None
    endDateOffsetInterval: int | None
    payoffStep: int | None
    payoffInterval: int | None


class ZenMoneyTag(TypedDict, total=False):
    """
    {
        "id": "84139eb3-f236-4c69-a4bd-0b0eeb8b6f18",
        "user": 686527,
        "changed": 1752395980,
        "icon": "2002_dancing",
        "budgetIncome": false,
        "budgetOutcome": false,
        "required": false,
        "archive": false,
        "showIncome": false,
        "showOutcome": true,
        "color": 4286605019,
        "picture": null,
        "title": "Развлечения",
        "parent": null,
        "staticId": "11"
    },
    """

    id: int
    user: int
    changed: int
    icon: str
    budgetIncome: bool
    budgetOutcome: bool
    required: bool
    archive: bool
    showIncome: bool
    showOutcome: bool
    color: int
    picture: str | None
    title: str
    parent: int | None
    staticId: str | None


class ZenMoneyBudget(TypedDict, total=False):
    """
    {
           "user": 686527,
           "changed": 1752395076,
           "date": "2025-07-01",
           "tag": "153ee0b5-26bc-4b18-b4bc-67d69ae59e81",
           "income": 0,
           "outcome": 10044,
           "incomeLock": true,
           "outcomeLock": true,
           "isIncomeForecast": false,
           "isOutcomeForecast": false
       },
    """

    user: int
    changed: int
    date: str
    tag: str
    income: int
    outcome: int
    incomeLock: bool
    outcomeLock: bool
    isIncomeForecast: bool
    isOutcomeForecast: bool


class ZenMoneyMerchant(TypedDict, total=False):
    """
    {
          "id": "7e688984-e2a9-4645-b52e-fd40aaf892a7",
          "user": 686527,
          "title": "Настоишная",
          "changed": 1670163709
      },
    """

    id: int
    user: int
    title: str
    changed: int


class ZenMoneyReminder(TypedDict, total=False):
    """
    {
        "id": "325a2550-5fc5-11f0-9461-79b36ca2f2e9",
        "user": 686527,
        "income": 1,
        "outcome": 0,
        "changed": 1752396097,
        "incomeInstrument": 2,
        "outcomeInstrument": 2,
        "step": 0,
        "points": [
            0
        ],
        "tag": null,
        "startDate": "2020-01-01",
        "endDate": "2020-01-01",
        "notify": false,
        "interval": null,
        "incomeAccount": "2a4ef0d0-5bff-11f0-b1dd-cf96e7eccef3",
        "outcomeAccount": "2a4ef0d0-5bff-11f0-b1dd-cf96e7eccef3",
        "comment": "{\"type\":\"EnvelopeMeta\",\"payload\":{\"tag#4b6debd0-4419-4384-815f-534d08fa53ad\":{\"id\":\"tag#4b6debd0-4419-4384-815f-534d08fa53ad\",\"visibility\":\"hidden\"}}}",
        "payee": null,
        "merchant": null
    },
    """

    id: str
    user: int
    income: int
    outcome: int
    changed: int
    incomeInstrument: int
    outcomeInstrument: int
    step: int
    points: list[int]
    tag: str | None
    startDate: str | None
    endDate: str | None
    notify: bool
    interval: str | None
    incomeAccount: str | None
    outcomeAccount: str | None
    comment: str | None
    payee: str | None
    merchant: str | None


class ZenMoneyReminderMarker(TypedDict, total=False):
    """
    {
           "id": "2f6fed81-9174-4231-a0cd-d7f04d75a62f",
           "user": 686527,
           "date": "2024-05-01",
           "income": 0,
           "outcome": 199,
           "changed": 1728589770,
           "incomeInstrument": 2,
           "outcomeInstrument": 2,
           "state": "processed",
           "isForecast": true,
           "reminder": "78670c65-d3b2-4bee-a55f-ada9a804785e",
           "incomeAccount": "20466600-54d7-4654-ae87-6a7ce14f12d1",
           "outcomeAccount": "20466600-54d7-4654-ae87-6a7ce14f12d1",
           "comment": null,
           "payee": "Tinkoff Pro",
           "merchant": null,
           "notify": false,
           "tag": null
       },
    """

    id: str
    user: int
    date: str
    income: int
    outcome: int
    changed: int
    incomeInstrument: int
    outcomeInstrument: int
    state: str
    isForecast: bool
    reminder: str
    incomeAccount: str | None
    outcomeAccount: str | None
    comment: str | None
    payee: str | None
    merchant: str | None
    notify: bool
    tag: str | None


class ZenMoneyTransaction(TypedDict, total=False):
    """
    {
          "id": "a033028b-faff-4cd4-84eb-11e459ac0c57",
          "user": 686527,
          "date": "2025-04-11",
          "income": 0,
          "outcome": 595,
          "changed": 1744362132,
          "incomeInstrument": 2,
          "outcomeInstrument": 2,
          "created": 1744360340,
          "originalPayee": "APTEKA ZDOROV.RU",
          "deleted": false,
          "viewed": false,
          "hold": false,
          "qrCode": null,
          "source": "plugin",
          "incomeAccount": "20466600-54d7-4654-ae87-6a7ce14f12d1",
          "outcomeAccount": "20466600-54d7-4654-ae87-6a7ce14f12d1",
          "tag": [
              "e2379555-db8e-4884-b59a-8036fd1ce0da"
          ],
          "comment": null,
          "payee": "APTEKA ZDOROV.RU",
          "opIncome": null,
          "opOutcome": null,
          "opIncomeInstrument": null,
          "opOutcomeInstrument": null,
          "latitude": null,
          "longitude": null,
          "merchant": null,
          "incomeBankID": null,
          "outcomeBankID": "[tinkoff][reg]-110766670972",
          "reminderMarker": null
      },
    """

    id: str
    user: int
    date: str
    income: int
    outcome: int
    changed: int
    incomeInstrument: int
    outcomeInstrument: int
    originalPayee: str
    deleted: bool
    viewed: bool
    hold: bool
    qrCode: str | None
    source: str
    incomeAccount: str | None
    outcomeAccount: str | None
    tag: list[str]
    comment: str | None
    payee: str | None
    opIncome: int | None
    opOutcome: int | None
    opIncomeInstrument: int | None
    opOutcomeInstrument: int | None
    latitude: str | None
    longitude: str | None
    merchant: str | None
    incomeBankID: str | None
    outcomeBankID: str | None
    reminderMarker: str | None


# endregion zen money models


class ZenMoneyDiffRaw(TypedDict, total=False):
    serverTimestamp: int
    instrument: list[ZenMoneyInstrument]
    country: list[ZenMoneyCountry]
    company: list[ZenMoneyCompany]
    user: list[ZenMoneyUser]
    account: list[ZenMoneyAccount]
    tag: list[ZenMoneyTag]
    budget: list[ZenMoneyBudget]
    merchant: list[ZenMoneyMerchant]
    reminder: list[ZenMoneyReminder]
    reminderMarker: list[ZenMoneyReminderMarker]
    transaction: list[ZenMoneyTransaction]


class ZenMoneyClient:
    """
    https://github.com/zenmoney/ZenPlugins/wiki/ZenMoney-API
    """

    def __init__(self, zen_money_token):
        self.zen_money_token = zen_money_token

    def diff(self, current_client_timestamp=None, server_timestamp=0) -> ZenMoneyDiffRaw:
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
