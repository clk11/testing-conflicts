"""Shopping cart and price calculation."""

from . import config


class Cart:
    def __init__(self, owner_email, customer_tier="standard"):
        self.owner_email = owner_email
        self.customer_tier = customer_tier
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

    def discount_rate(self):
        """Best rate the cart qualifies for, by volume or by customer tier."""
        count = self.item_count()
        rate = 0.0
        for threshold, tier_rate in config.VOLUME_DISCOUNT_TIERS:
            if count >= threshold:
                rate = tier_rate
        if self.customer_tier == "wholesale":
            rate = max(rate, config.WHOLESALE_DISCOUNT)
        return rate

    def discount(self, subtotal):
        return round(subtotal * self.discount_rate(), 2)

    def total(self):
        subtotal = self.subtotal()
        discount = self.discount(subtotal)
        discounted = round(subtotal - discount, 2)
        # Shipping follows the amount actually charged, so a big discount can
        # push an order back under the free-shipping threshold.
        shipping = self.shipping(discounted)
        tax = round(discounted * config.TAX_RATE, 2)
        return {
            "subtotal": subtotal,
            "discount": discount,
            "discount_rate": self.discount_rate(),
            "shipping": shipping,
            "tax": tax,
            "grand_total": round(discounted + shipping + tax, 2),
        }
