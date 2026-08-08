# ShopKit

A tiny, dependency-free shop backend used as a playground.

## Features

- Email + password accounts with expiring sessions
- A cart that merges duplicate SKUs and computes tax and shipping
- An in-memory inventory with reservations that can be released or committed
- An order flow that ties the three together

## Running the demo

```sh
python demo.py
```

## Layout

| File                   | Responsibility                        |
| ---------------------- | ------------------------------------- |
| `shopkit/config.py`    | Tunable constants                     |
| `shopkit/auth.py`      | Registration, login, sessions         |
| `shopkit/cart.py`      | Line items and price calculation      |
| `shopkit/inventory.py` | Stock levels and reservations         |
| `shopkit/orders.py`    | Placing an order                      |
