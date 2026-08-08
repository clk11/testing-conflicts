"""Application configuration."""

APP_NAME = "ShopKit"
VERSION = "0.1.5"

# Pricing
CURRENCY = "USD"
TAX_RATE = 0.21
FREE_SHIPPING_THRESHOLD = 75.0
SHIPPING_FLAT_FEE = 9.99

# Volume discounts: (minimum item count, percentage off)
VOLUME_DISCOUNT_TIERS = (
    (10, 0.10),
    (25, 0.15),
    (50, 0.20),
)
WHOLESALE_DISCOUNT = 0.25

# Auth
SESSION_TTL_SECONDS = 3600
MIN_PASSWORD_LENGTH = 10
MAX_LOGIN_ATTEMPTS = 5
LOGIN_LOCKOUT_SECONDS = 900
