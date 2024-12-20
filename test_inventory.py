import sqlite3
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
    Inventory.add_product("Test Product", "Description", 10, 5.99, 1)
    Inventory.add_product("Another Product", "Another Description", 21, 10.99, 1)
    yield
    os.remove("inventory_test.db")


def test_initialize_db(setup_database):
    assert os.path.exists("inventory_test.db"), "Database file should be created."

def test_get_categories(setup_database):
    categories = Inventory.get_categories()
    assert len(categories) > 0, "There should be categories in the database."

def test_category_exists(setup_database):
    assert Inventory.category_exists(1), "Category with ID 1 should exist."

def test_category_not_exists(setup_database):
    assert not Inventory.category_exists(999), "Category with ID 2 should not exist."

def test_get_category(setup_database):
    category = Inventory.get_category(1)
    assert category is not None, "Category with ID 1 should exist."
    assert category[1] == "Electronics", "Category name should match."

def test_add_product(setup_database):
    Inventory.add_product("Another Product", "Another Description", 20, 10.99, 2)
    products = Inventory.get_products()
    assert len(products) == 3, "There should be 2 products in the database."
    assert products[1][1] == "Another Product", "Second product name should match."

def test_add_product_invalid_price(setup_database):
    with pytest.raises(sqlite3.IntegrityError):
        Inventory.add_product("Invalid Product", "Description", 10, "Invalid Price", 1)

def test_add_product_invalid_quantity(setup_database):
    with pytest.raises(sqlite3.IntegrityError):
        Inventory.add_product("Invalid Product", "Description", "Invalid Quantity", 5.99, 1)

def test_add_product_negative_quantity(setup_database):
    with pytest.raises(sqlite3.IntegrityError):
        Inventory.add_product("Invalid Product", "Description", -10, 5.99, 1)

def test_add_product_negative_price(setup_database):
    with pytest.raises(sqlite3.IntegrityError):
        Inventory.add_product("Invalid Product", "Description", 10, -5.99, 1)

def test_add_product_zero_price(setup_database):
    with pytest.raises(sqlite3.IntegrityError):
        Inventory.add_product("Invalid Product", "Description", 10, 0, 1)

def test_add_product_nonexistent_category(setup_database):
    with pytest.raises(sqlite3.IntegrityError):
        Inventory.add_product("Invalid Product", "Description", 10, 5.99, 999)

def test_get_products(setup_database):
    products = Inventory.get_products()
    assert len(products) > 0, "Should return at least one product."
    assert products[0][1] == "Test Product", "First product name should match."

def test_find_product(setup_database):
    product = Inventory.find_product_by_id(1)
    assert product is not None, "Product with ID 1 should exist."
    assert product[1] == "Test Product", "Product name should match."

def test_find_product_by_name(setup_database):
    product = Inventory.find_product_by_name("Test Product")
    assert product is not None, "Product with name 'Test Product' should exist."
    assert product[1] == "Test Product", "Product name should match."

def test_find_products_by_category(setup_database):
    products = Inventory.find_products_by_category(1)
    assert len(products) == 2, "There should be 2 products in category ID 1."
    assert products[0][1] == "Test Product", "First product name should match."

def test_update_product(setup_database):
    success = Inventory.update_product(1, "quantity", 5)
    assert success, "Update should succeed for existing product."
    product = Inventory.find_product_by_id(1)
    assert product[3] == 5, "Product quantity should be updated."

def test_update_product_invalid_attribute(setup_database):
    with pytest.raises(sqlite3.OperationalError):
        Inventory.update_product(1, "invalid_attribute", 5)

def test_update_product_negative_quantity(setup_database):
    with pytest.raises(sqlite3.IntegrityError):
        Inventory.update_product(1, "quantity", -5)

def test_update_product_negative_price(setup_database):
    with pytest.raises(sqlite3.IntegrityError):
        Inventory.update_product(1, "price", -5.99)

def test_update_product_zero_price(setup_database):
    with pytest.raises(sqlite3.IntegrityError):
        Inventory.update_product(1, "price", 0)

def test_update_product_invalid_price(setup_database):
    with pytest.raises(sqlite3.IntegrityError):
        Inventory.update_product(1, "price", "invalid_price")

def test_update_product_invalid_quantity(setup_database):
    with pytest.raises(sqlite3.IntegrityError):
        Inventory.update_product(1, "quantity", "invalid_quantity")

def test_update_product_nonexistent_product(setup_database):
    success = Inventory.update_product(999, "quantity", 5)
    assert not success, "Update should fail for nonexistent product."

def test_delete_product(setup_database):
    success = Inventory.delete_product(1)
    assert success, "Delete should succeed for existing product."
    product = Inventory.find_product_by_id(1)
    assert product is None, "Product should no longer exist in the database."

def test_delete_product_nonexistent_product(setup_database):
    success = Inventory.delete_product(999)
    assert not success, "Delete should fail for nonexistent product."

def test_products_low_stock(setup_database):
    low_stock_products = Inventory.products_low_stock(20)
    assert len(low_stock_products) == 1, "Should return one low stock product."
    assert low_stock_products[0][1] == "Test Product", "Low stock product name should match."

def test_products_low_stock_no_results(setup_database):
    low_stock_products = Inventory.products_low_stock(1)
    assert len(low_stock_products) == 0, "There should be no products with stock <= 1."

