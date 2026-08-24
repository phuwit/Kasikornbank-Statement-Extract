from dataclasses import dataclass
from typing import Literal


@dataclass
class Transaction:
    date: str
    time: str
    description: str
    txn_type: Literal["deposit", "withdrawal"]
    withdrawal: bool
    amount: str
    balance: str
    channel: str
    details: str

    @staticmethod
    def get_csv_header() -> str:
        return "date,time,description,txn_type,withdrawal,amount,balance,channel,details"

    def __str__(self) -> str:
        return f"{self.date},{self.time},{self.description},{self.txn_type},{self.withdrawal},{self.amount},{self.balance},{self.channel},{self.details}"



@dataclass
class BoundingBox:
    width: float
    top: float
    left: float
