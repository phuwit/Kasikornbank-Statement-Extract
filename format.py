from dataclasses import dataclass
import re
import sys


transaction_pattern = re.compile(r"^(?P<date>\d\d-\d\d-\d\d)\s(?P<time>\d\d:\d\d)\s(?P<txn_type>.+?)\s(?P<amount>[\d,]+?\.\d\d)\s(?P<balance>[\d,]+?\.\d\d)\s(?P<description>.+)$")

keys = ['date', 'time', 'txn_type', 'amount', 'balance', 'description']

@dataclass
class Transaction():
    date: str
    time: str
    txn_type: str
    amount: str
    balance: str
    description: str

    def __str__(self) -> str:
        return f'{self.date},{self.time},{self.txn_type},{self.amount},{self.balance},{self.description}'

def clean_text(text: str) -> str:
    return text.replace(',', '')


def main():
    filename = sys.argv[1]

    csv_contents = f'{','.join(keys)}\n'

    with open(filename, mode='rt') as file:
        for line in file.readlines():
            line = line.strip()
            result = transaction_pattern.match(line)
            try:
                transaction = Transaction(
                    date=clean_text(result['date']),
                    time=clean_text(result['time']),
                    txn_type=clean_text(result['txn_type']),
                    amount=clean_text(result['amount']),
                    balance=clean_text(result['balance']),
                    description=clean_text(result['description'])
                )
                if 'deposit' not in transaction.txn_type.lower():
                    transaction.amount = f'-{transaction.amount}'
                csv_contents += f'{str(transaction)}\n'
            except TypeError:
                print(f'line "{line}" is not convertable')

    with open(f'{filename}.csv', mode='wt') as file:
        file.write(csv_contents)


if __name__ == "__main__":
    main()
