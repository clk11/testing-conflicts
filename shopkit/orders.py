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

    def place_order(self, token, cart, coupon_code=None):
        email = self.auth.resolve(token)
        if email is None:
            raise OrderError("session expired")
        if not cart.lines:
            raise OrderError("cart is empty")

        if coupon_code:
            cart.apply_coupon(coupon_code)

        order_id = uuid.uuid4().hex
        try:
            for line in cart.lines:
                self.inventory.reserve(order_id, line["sku"], line["quantity"])
        except InventoryError as exc:
            self.inventory.release(order_id)
            raise OrderError(str(exc)) from exc

        totals = cart.total()
        order = {
            "id": order_id,
            "email": email,
            "lines": [dict(line) for line in cart.lines],
            "totals": totals,
            "coupon": totals["coupon"],
            "loyalty_points": totals["loyalty_points"],
            "status": "confirmed",
        }
        self.orders[order_id] = order
        self.inventory.commit(order_id)
        return order

    def get(self, order_id):
        return self.orders.get(order_id)
