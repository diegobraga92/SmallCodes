'''
Enunciado

O código abaixo tem problemas. Identifique e corrija.

class UserService:
    users = []

    def add(self, user):
        self.users.append(user)

    def get_all(self):
        return self.users
'''

class UserService:
    def __init__(self):
        self._users = []

    def add(self, user: dict):
        if "email" not in user:
            raise ValueError("email is required")

        self._users.append(user)

    def get_all(self) -> list[dict]:
        return list(self._users)
