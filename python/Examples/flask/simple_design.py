'''
Enunciado

Crie um serviço de carrinho de compras.

Requisitos

Adicionar item (nome + preço)

Remover item

Calcular total

Não permitir preços negativos
'''

class ShoppingCart:
    def __init__(self):
        self._items = []

    def add_item(self, name: str, price: float):
        if price <= 0:
            raise ValueError("Invalid price")

        self._items.append({"name": name, "price": price})

    def remove_item(self, name: str):
        self._items = [
            item for item in self._items if item["name"] != name
        ]

    def total(self) -> float:
        return sum(item["price"] for item in self._items)
