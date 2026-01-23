'''
Enunciado

Refatore o código abaixo para torná-lo mais legível e extensível:

def process(order):
    if order["type"] == "food":
        return order["price"] * 0.9
    elif order["type"] == "electronics":
        return order["price"] * 0.8
    elif order["type"] == "books":
        return order["price"] * 0.95
'''

DISCOUNTS = {
    "food": 0.9,
    "electronics": 0.8,
    "books": 0.95,
}


def calculate_price(order: dict) -> float:
    order_type = order.get("type")
    price = order.get("price", 0)

    if order_type not in DISCOUNTS:
        raise ValueError("Invalid order type")

    return price * DISCOUNTS[order_type]
