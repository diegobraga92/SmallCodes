'''
Enunciado

Escreva 1 teste unitário para a classe BankAccount.
'''

import pytest
from bank import BankAccount


def test_deposit_increases_balance():
    account = BankAccount("Ana", 100)

    account.deposit(50)

    assert account.balance == 150
