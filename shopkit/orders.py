"""Order placement flow."""

import uuid

from .inventory import InventoryError


class OrderError(Exception):
    """Raised when an order cannot be placed."""


class OrderService:
    def __init__(self, auth, inventory):
        self.auth = auth
        self.inventory = inventory
        self.orders = {}

    def place_order(self, token, cart):
        email = self.auth.resolve(token)
        if email is None:
            raise OrderError("session expired")
        if not cart.lines:
            raise OrderError("cart is empty")

        order_id = uuid.uuid4().hex
        backorders_before = len(self.inventory.backorders)
        try:
            for line in cart.lines:
                self.inventory.reserve(order_id, line["sku"], line["quantity"])
        except InventoryError as exc:
            self.inventory.release(order_id)
            raise OrderError(str(exc)) from exc

        backordered = len(self.inventory.backorders) > backorders_before

        totals = cart.total()
        order = {
            "id": order_id,
            "email": email,
            "tier": cart.customer_tier,
            "lines": [dict(line) for line in cart.lines],
            "totals": totals,
            "discount": totals["discount"],
            "status": "backordered" if backordered else "confirmed",
        }
        self.orders[order_id] = order
        self.inventory.commit(order_id)
        return order

    def get(self, order_id):
        return self.orders.get(order_id)
