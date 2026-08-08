"""Shopping cart and price calculation."""

from . import config


class Cart:
    def __init__(self, owner_email):
        self.owner_email = owner_email
        self.lines = []

    def add_item(self, sku, unit_price, quantity=1):
        if quantity < 1:
            raise ValueError("quantity must be positive")

        for line in self.lines:
            if line["sku"] == sku:
                line["quantity"] += quantity
                return line

        line = {"sku": sku, "unit_price": unit_price, "quantity": quantity}
        self.lines.append(line)
        return line

    def remove_item(self, sku):
        self.lines = [line for line in self.lines if line["sku"] != sku]

    def item_count(self):
        return sum(line["quantity"] for line in self.lines)

    def subtotal(self):
        return round(
            sum(line["unit_price"] * line["quantity"] for line in self.lines), 2
        )

    def shipping(self, amount):
        if amount >= config.FREE_SHIPPING_THRESHOLD:
            return 0.0
        return config.SHIPPING_FLAT_FEE

    def total(self):
        subtotal = self.subtotal()
        shipping = self.shipping(subtotal)
        tax = round(subtotal * config.TAX_RATE, 2)
        return {
            "subtotal": subtotal,
            "shipping": shipping,
            "tax": tax,
            "grand_total": round(subtotal + shipping + tax, 2),
        }
