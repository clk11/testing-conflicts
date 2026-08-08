"""Tiny end-to-end walkthrough of the shopkit flow."""

from shopkit.auth import AuthService
from shopkit.cart import Cart
from shopkit.inventory import Inventory
from shopkit.orders import OrderService


def main():
    auth = AuthService()
    inventory = Inventory(allow_backorders=True)
    orders = OrderService(auth, inventory)

    auth.register("ada@example.com", "correcthorsebattery")
    token = auth.login("ada@example.com", "correcthorsebattery")

    inventory.restock("KB-01", 40)
    inventory.restock("MS-02", 15)

    cart = Cart("ada@example.com", customer_tier="wholesale")
    cart.add_item("KB-01", 79.0, quantity=12)
    cart.add_item("MS-02", 25.5, quantity=1)

    order = orders.place_order(token, cart)
    print(f"order {order['id']} -> {order['status']}")
    print(f"tier: {order['tier']} (saved {order['discount']})")
    for key, value in order["totals"].items():
        print(f"  {key}: {value}")

    for alert in inventory.alerts:
        print(f"! {alert}")


if __name__ == "__main__":
    main()
