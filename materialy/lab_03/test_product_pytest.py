# -*- coding: utf-8 -*-
"""Testy pytest dla klasy Product -- uzupelnij!

Uruchomienie: pytest test_product_pytest.py -v
"""

import pytest
from product import Product


# --- Fixture ---

@pytest.fixture
def product():
    """Tworzy instancje Product do testow (odpowiednik setUp)."""
    # TODO: Zwroc instancje Product, np. Product("Laptop", 2999.99, 10)
    return Product("Laptop", 2999.99, 10)


# --- Testy z fixture ---

def test_is_available(product):
    """Sprawdz dostepnosc produktu."""
    # TODO: Uzyj assert product.is_available() == True
    assert product.is_available() == True


def test_total_value(product):
    """Sprawdz wartosc calkowita."""
    # TODO: Uzyj assert product.total_value() == oczekiwana_wartosc
    assert product.total_value() == pytest.approx(29999.9)


# --- Testy z parametryzacja ---

@pytest.mark.parametrize("amount, expected_quantity", [
    # TODO: Dodaj przypadki testowe jako krotki, np.:
    (5, 15),   # dodanie 5 do poczatkowych 10 = 15
    (0, 10),   # dodanie 0 = bez zmian
    (100, 110),  # dodanie 100
])
def test_add_stock_parametrized(product, amount, expected_quantity):
    """Testuje add_stock z roznymi wartosciami."""
    # TODO: Wywolaj product.add_stock(amount) i sprawdz product.quantity
    product.add_stock(amount)
    assert product.quantity == expected_quantity


# --- Testy bledow ---

def test_remove_stock_too_much_raises(product):
    """Sprawdz, czy proba usuniecia za duzej ilosci rzuca ValueError."""
    # TODO: Uzyj with pytest.raises(ValueError):
    with pytest.raises(ValueError):
        product.remove_stock(999)


def test_add_stock_negative_raises(product):
    """Sprawdz, czy ujemna wartosc w add_stock rzuca ValueError."""
    # TODO: Uzyj with pytest.raises(ValueError):
    with pytest.raises(ValueError):
        product.add_stock(-5)

def test_remove_stock_positive(product):
    product.remove_stock(3)
    assert product.quantity == 7


def test_is_not_available_when_empty():
    empty_product = Product("Mouse", 99.99, 0)
    assert empty_product.is_available() is False

@pytest.mark.parametrize("percent, expected_price", [
    (0, 2999.99),
    (50, 1499.995),
    (100, 0.0),
])
def test_apply_discount(product, percent, expected_price):
    product.apply_discount(percent)
    assert product.price == pytest.approx(expected_price)

@pytest.mark.parametrize("percent", [-10, 120])
def test_apply_discount_invalid_percent_raises(product, percent):
    with pytest.raises(ValueError):
        product.apply_discount(percent)
