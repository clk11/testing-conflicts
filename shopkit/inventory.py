"""In-memory inventory with expiring reservations."""

import time

DEFAULT_RESERVATION_TTL = 900


class InventoryError(Exception):
    """Raised when stock cannot satisfy a request."""


class Inventory:
    def __init__(self, clock=time.time, reservation_ttl=DEFAULT_RESERVATION_TTL):
        self._clock = clock
        self.reservation_ttl = reservation_ttl
        self._stock = {}
        self._reservations = {}

    def restock(self, sku, quantity):
        self._stock[sku] = self._stock.get(sku, 0) + quantity
        return self._stock[sku]

    def available(self, sku):
        return self._stock.get(sku, 0)

    def reserve(self, order_id, sku, quantity):
        self.expire_stale()

        available = self.available(sku)
        if quantity > available:
            raise InventoryError(f"not enough stock for {sku}")

        self._stock[sku] = available - quantity
        self._reservations.setdefault(order_id, []).append(
            {
                "sku": sku,
                "quantity": quantity,
                "expires_at": self._clock() + self.reservation_ttl,
            }
        )
        return self._stock[sku]

    def expire_stale(self):
        """Hand back stock held by carts that were abandoned."""
        now = self._clock()
        expired = 0
        for order_id, items in list(self._reservations.items()):
            live = []
            for item in items:
                if item["expires_at"] <= now:
                    self._stock[item["sku"]] = (
                        self._stock.get(item["sku"], 0) + item["quantity"]
                    )
                    expired += 1
                else:
                    live.append(item)
            if live:
                self._reservations[order_id] = live
            else:
                del self._reservations[order_id]
        return expired

    def release(self, order_id):
        for item in self._reservations.pop(order_id, []):
            self._stock[item["sku"]] = (
                self._stock.get(item["sku"], 0) + item["quantity"]
            )

    def commit(self, order_id):
        self._reservations.pop(order_id, None)
