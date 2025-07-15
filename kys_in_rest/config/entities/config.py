from pydantic import BaseModel


class Config(BaseModel):
    zen_money_server_timestamp: int = 0