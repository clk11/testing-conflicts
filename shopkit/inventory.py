"""In-memory inventory with simple reservations."""

import time


class InventoryError(Exception):
    """Raised when stock cannot satisfy a request."""


class Inventory:
    def __init__(self, clock=time.time):
        self._clock = clock
        self._stock = {}
        self._reservations = {}

    def restock(self, sku, quantity):
        self._stock[sku] = self._stock.get(sku, 0) + quantity
        return self._stock[sku]

    def available(self, sku):
        return self._stock.get(sku, 0)

    def reserve(self, order_id, sku, quantity):
        available = self.available(sku)
        if quantity > available:
            raise InventoryError(f"not enough stock for {sku}")

        self._stock[sku] = available - quantity
        self._reservations.setdefault(order_id, []).append(
            {"sku": sku, "quantity": quantity}
        )
        return self._stock[sku]

    def release(self, order_id):
        for item in self._reservations.pop(order_id, []):
            self._stock[item["sku"]] = (
                self._stock.get(item["sku"], 0) + item["quantity"]
            )

    def commit(self, order_id):
        self._reservations.pop(order_id, None)
