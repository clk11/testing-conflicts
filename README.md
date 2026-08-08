# ShopKit

A tiny, dependency-free shop backend used as a playground.

## Features

- Email + password accounts, with salted and stretched password hashes
- An audit trail of every registration and login attempt
- Coupon codes (`WELCOME10`, `VIP20`) applied at checkout
- Loyalty points awarded per unit purchased
- Reservations that expire on their own so abandoned carts free their stock

## Running the demo

```sh
python demo.py
```

## Layout

| File                   | Responsibility                          |
| ---------------------- | --------------------------------------- |
| `shopkit/config.py`    | Constants, coupon table, hash rounds    |
| `shopkit/auth.py`      | Registration, login, sessions, auditing |
| `shopkit/cart.py`      | Line items, coupons, loyalty points     |
| `shopkit/inventory.py` | Stock levels and expiring reservations  |
| `shopkit/orders.py`    | Placing an order                        |
