import pytest
import os
from inventory import Inventory

@pytest.fixture(scope="function")
def setup_database():
    Inventory.initialize_db("inventory_test.db")
    connection = Inventory.connect_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM products")
    connection.commit()
    connection.close()
    Inventory.add_product("Test Product", "Description", 10, 5.99, "Test Category")
    yield
    os.remove("inventory_test.db")

def test_initialize_db(setup_database):
    assert os.path.exists("inventory_test.db"), "Database file should be created."

def test_add_product(setup_database):
    Inventory.add_product("Another Product", "Another Description", 20, 10.99, "Misc")
    products = Inventory.get_products()
    assert len(products) == 2, "There should be 2 products in the database."
    assert products[1][1] == "Another Product", "Second product name should match."

def test_get_products(setup_database):
    products = Inventory.get_products()
    assert len(products) > 0, "Should return at least one product."
    assert products[0][1] == "Test Product", "First product name should match."

def test_find_product(setup_database):
    product = Inventory.find_product_by_id(1)
    assert product is not None, "Product with ID 1 should exist."
    assert product[1] == "Test Product", "Product name should match."

def test_update_product(setup_database):
    success = Inventory.update_product(1, "quantity", 5)
    assert success, "Update should succeed for existing product."
    product = Inventory.find_product_by_id(1)
    assert product[3] == 5, "Product quantity should be updated."

def test_delete_product(setup_database):
    success = Inventory.delete_product(1)
    assert success, "Delete should succeed for existing product."
    product = Inventory.find_product_by_id(1)
    assert product is None, "Product should no longer exist in the database."

def test_products_low_stock(setup_database):
    low_stock_products = Inventory.products_low_stock(20)
    assert len(low_stock_products) == 1, "Should return one low stock product."
    assert low_stock_products[0][1] == "Test Product", "Low stock product name should match."
