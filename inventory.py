import sqlite3


class Inventory:
    db_name = ''

    @staticmethod
    def connect_db():
        return sqlite3.connect(Inventory.db_name)

    @staticmethod
    def set_db_name(db_name):
        Inventory.db_name = db_name

    @staticmethod
    def initialize_db(db_name_env):
        Inventory.set_db_name(db_name_env)
        connection = Inventory.connect_db()
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                category TEXT
            )
        ''')
        connection.commit()
        connection.close()

    @staticmethod
    def add_product(name, description, quantity, price, category):
        connection = Inventory.connect_db()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO products (name, description, quantity, price, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, description, quantity, price, category))
        connection.commit()
        connection.close()

    @staticmethod
    def get_products():
        connection = Inventory.connect_db()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        connection.close()
        return products

    @staticmethod
    def update_product(product_id, attribute, new_value):
        connection = Inventory.connect_db()
        cursor = connection.cursor()
        cursor.execute(f'''
            UPDATE products
            SET {attribute} = ?
            WHERE id = ?
        ''', (new_value, product_id))
        changes = cursor.rowcount
        connection.commit()
        connection.close()
        return changes > 0

    @staticmethod
    def delete_product(product_id):
        connection = Inventory.connect_db()
        cursor = connection.cursor()
        cursor.execute('''
            DELETE FROM products
            WHERE id = ?
        ''', (product_id,))
        changes = cursor.rowcount
        connection.commit()
        connection.close()
        return changes > 0

    @staticmethod
    def find_product(product_id):
        connection = Inventory.connect_db()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = cursor.fetchone()
        connection.close()
        return product

    @staticmethod
    def products_low_stock(limit):
        connection = Inventory.connect_db()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM products WHERE quantity <= ?', (limit,))
        products = cursor.fetchall()
        connection.close()
        return products
