"""In-memory inventory with reservations, alerts and backorders."""

import time

DEFAULT_LOW_STOCK_THRESHOLD = 5


class InventoryError(Exception):
    """Raised when stock cannot satisfy a request."""


class Inventory:
    def __init__(
        self,
        clock=time.time,
        allow_backorders=False,
        low_stock_threshold=DEFAULT_LOW_STOCK_THRESHOLD,
    ):
        self._clock = clock
        self.allow_backorders = allow_backorders
        self.low_stock_threshold = low_stock_threshold
        self.alerts = []
        self.backorders = []
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
            if not self.allow_backorders:
                raise InventoryError(f"not enough stock for {sku}")
            self.backorders.append(
                {"sku": sku, "quantity": quantity - available}
            )
            quantity = available

        self._stock[sku] = available - quantity
        if self._stock[sku] <= self.low_stock_threshold:
            self.alerts.append(f"low stock: {sku} ({self._stock[sku]} left)")
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
