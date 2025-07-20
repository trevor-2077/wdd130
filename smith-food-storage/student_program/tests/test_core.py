import pytest
from datetime import date, timedelta
from student_program.core import get_expiring_items, total_inventory_value

def test_get_expiring_items(monkeypatch):
    today = date(2025, 7, 20)
    monkeypatch.setattr('student_program.core.date.today', lambda: today)

    class FakeItem: 
        def __init__(self, name, expires, quantity):
            self.name, self.expires, self.quantity = name, expires, quantity
    fake_rows = [
        FakeItem("Milk", today + timedelta(days=2), 1),
        FakeItem("Bread", today + timedelta(days=5), 2),
    ]
    monkeypatch.setattr('student_program.core.Item.query.filter', 
                        lambda *args, **kwargs: fake_rows)
    result = get_expiring_items(3)
    assert result == [{'name': 'Milk', 'expires': today + timedelta(days=2), 'quantity': 1}]

def test_total_inventory_value(monkeypatch):
    
    class FakeItem:
        def __init__(self, quantity, purchase_price):
            self.quantity, self.purchase_price = quantity, purchase_price
    fake_items = [FakeItem(2, 3.50), FakeItem(1, 4.00)]
    monkeypatch.setattr('student_program.core.Item.query.filter', 
                        lambda *args, **kwargs: fake_items)
    total = total_inventory_value()
    assert total == 2*3.50 + 1*4.00
