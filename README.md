# ShopKit

A tiny, dependency-free shop backend used as a playground.

## Features

- Email + password accounts, with lockout after repeated failed logins
- SHA-512 password digests and a longer minimum password
- Volume discount tiers, plus a flat wholesale rate for trade customers
- Low-stock alerts and optional backorders when stock runs out

## Running the demo

```sh
python demo.py
```

## Layout

| File                   | Responsibility                         |
| ---------------------- | -------------------------------------- |
| `shopkit/config.py`    | Constants, discount tiers, lockout      |
| `shopkit/auth.py`      | Registration, login, lockout, sessions  |
| `shopkit/cart.py`      | Line items, tiers, volume discounts     |
| `shopkit/inventory.py` | Stock levels, alerts, backorders        |
| `shopkit/orders.py`    | Placing an order                        |
