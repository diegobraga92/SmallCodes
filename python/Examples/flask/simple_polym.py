'''
Enunciado

Implemente um sistema de notificações.

Requisitos

Tipos de notificação:

Email

SMS

Todas devem ter um método:

send(message: str) -> None


Criar uma função que envia uma mensagem para uma lista de notificadores
'''


from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass


class EmailNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"Sending EMAIL: {message}")


class SMSNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"Sending SMS: {message}")


def notify_all(notifiers: list[Notifier], message: str):
    for notifier in notifiers:
        notifier.send(message)


if __name__ == "__main__":
    notifiers = [EmailNotifier(), SMSNotifier()]
    notify_all(notifiers, "Hello!")
