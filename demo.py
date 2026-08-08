"""Tiny end-to-end walkthrough of the shopkit flow."""

from shopkit.auth import AuthService
from shopkit.cart import Cart
from shopkit.inventory import Inventory
from shopkit.orders import OrderService


def main():
    auth = AuthService()
    inventory = Inventory()
    orders = OrderService(auth, inventory)

    auth.register("ada@example.com", "correcthorse")
    token = auth.login("ada@example.com", "correcthorse")

    inventory.restock("KB-01", 40)
    inventory.restock("MS-02", 15)

    cart = Cart("ada@example.com")
    cart.add_item("KB-01", 79.0, quantity=2)
    cart.add_item("MS-02", 25.5, quantity=1)

    order = orders.place_order(token, cart)
    print(f"order {order['id']} -> {order['status']}")
    for key, value in order["totals"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
