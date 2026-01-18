'''
Enunciado

Implemente um pequeno sistema de conta bancária usando OOP.

Requisitos

Uma conta tem:

owner

balance

Operações:

deposit(amount)

withdraw(amount)

Regras:

Não permitir valores negativos

Não permitir saque maior que o saldo

O saldo não pode ser alterado diretamente
'''


class BankAccount:
    def __init__(self, owner: str, balance: float = 0):
        if balance < 0:
            raise ValueError("Initial balance cannot be negative")

        self._owner = owner
        self._balance = balance

    @property
    def owner(self):
        return self._owner

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        self._balance += amount

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive")

        if amount > self._balance:
            raise ValueError("Insufficient funds")

        self._balance -= amount
