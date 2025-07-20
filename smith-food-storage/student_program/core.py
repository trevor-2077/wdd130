from typing import Any
from datetime import date, timedelta
from models import Item, Location, db

def get_expiring_items(days: int) -> list[dict]:
    cutoff = date.today() + timedelta(days=days)
    rows = (Item.query
            .filter(Item.expires != None)
            .filter(Item.expires <= cutoff)
            .all())
    return [
        {'name': i.name, 'expires': i.expires, 'quantity': i.quantity}
        for i in rows
    ]

def total_inventory_value() -> float:
    items = Item.query.filter(Item.purchase_price != None).all()
    total = sum((i.quantity or 0) * float(i.purchase_price or 0) for i in items)
    return round(total, 2)

def count_by_location() -> dict[str, int]:
    from collections import Counter
    joins = db.session.query(Location.name, Item.item_id) \
        .join(Item, Item.location_id == Location.location_id) \
        .all()
    counter = Counter(name for name, _ in joins)
    return dict(counter)

def format_report(data: Any) -> str:
    if isinstance(data, list):
        lines = [f"{it['name']} (x{it['quantity']}) expires {it['expires']}" for it in data]
        return "\n".join(lines) or "No items."
    elif isinstance(data, dict):
        lines = [f"{k}: {v}" for k, v in data.items()]
        return "\n".join(lines) or "No data."
    elif isinstance(data, (int, float)):
        return f"${data:.2f}"
    else:
        return str(data)


