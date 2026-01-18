'''
nunciado

Você recebe uma lista de transações financeiras:

transactions = [
    {"id": 1, "user": "ana", "amount": 100, "type": "credit"},
    {"id": 2, "user": "ana", "amount": 50, "type": "debit"},
    {"id": 3, "user": "bruno", "amount": 75, "type": "credit"},
    {"id": 4, "user": "ana", "amount": 25, "type": "debit"},
]

Tarefas

Calcule o saldo final por usuário

Retorne um dicionário no formato:

{
    "ana": 25,
    "bruno": 75
}


Regras

credit soma

debit subtrai

Código deve ser legível e testável
'''

from collections import defaultdict
from typing import List, Dict


def calculate_balances(transactions: List[dict]) -> Dict[str, int]:
    balances = defaultdict(int)

    for tx in transactions:
        user = tx["user"]
        amount = tx["amount"]
        tx_type = tx["type"]

        if tx_type == "credit":
            balances[user] += amount
        elif tx_type == "debit":
            balances[user] -= amount

    return dict(balances)


if __name__ == "__main__":
    transactions = [
        {"id": 1, "user": "ana", "amount": 100, "type": "credit"},
        {"id": 2, "user": "ana", "amount": 50, "type": "debit"},
        {"id": 3, "user": "bruno", "amount": 75, "type": "credit"},
        {"id": 4, "user": "ana", "amount": 25, "type": "debit"},
    ]

    print(calculate_balances(transactions))
