"""Shopping cart and price calculation."""

from . import config


class Cart:
    def __init__(self, owner_email):
        self.owner_email = owner_email
        self.coupon_code = None
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

    def apply_coupon(self, code):
        if code not in config.COUPON_CODES:
            raise ValueError(f"unknown coupon: {code}")
        self.coupon_code = code
        return self.coupon_code

    def discount(self, subtotal):
        """Percentage off driven by the coupon the shopper applied."""
        if self.coupon_code is None:
            return 0.0
        rate = config.COUPON_CODES.get(self.coupon_code, 0.0)
        return round(subtotal * rate, 2)

    def loyalty_points(self):
        return self.item_count() * config.LOYALTY_POINTS_PER_UNIT

    def total(self):
        subtotal = self.subtotal()
        discount = self.discount(subtotal)
        discounted = round(subtotal - discount, 2)
        # Shipping is judged on the pre-coupon subtotal so a coupon never
        # silently costs the shopper their free shipping.
        shipping = self.shipping(subtotal)
        tax = round(discounted * config.TAX_RATE, 2)
        return {
            "subtotal": subtotal,
            "coupon": self.coupon_code,
            "discount": discount,
            "shipping": shipping,
            "tax": tax,
            "loyalty_points": self.loyalty_points(),
            "grand_total": round(discounted + shipping + tax, 2),
        }
