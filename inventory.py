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
                id_category INTEGER,
                FOREIGN KEY (id_category) REFERENCES categories(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')

        cursor.execute('''
            INSERT OR IGNORE INTO categories (name)
            VALUES ('Electronics')
        ''')
        cursor.execute('''
            INSERT OR IGNORE INTO categories (name)
            VALUES ('Clothing')
        ''')
        cursor.execute('''
            INSERT OR IGNORE INTO categories (name)
            VALUES ('Books')
        ''')

        connection.commit()
        connection.close()

    @staticmethod
    def add_product(name, description, quantity, price, id_category):
        connection = Inventory.connect_db()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO products (name, description, quantity, price, id_category)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, description, quantity, price, id_category))
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
        if not Inventory.find_product(product_id):
            return False
        connection = Inventory.connect_db()
        cursor = connection.cursor()
        cursor.execute(f'''
            UPDATE products
            SET {attribute} = ?
            WHERE id = ?
        ''', (new_value, product_id))
        connection.commit()
        connection.close()
        return True

    @staticmethod
    def delete_product(product_id):
        if not Inventory.find_product(product_id):
            return False
        connection = Inventory.connect_db()
        cursor = connection.cursor()
        cursor.execute('''
            DELETE FROM products
            WHERE id = ?
        ''', (product_id,))
        connection.commit()
        connection.close()
        return True

    @staticmethod
    def find_product_by_id(product_id):
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

    @staticmethod
    def get_categories():
        connection = Inventory.connect_db()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM categories')
        categories = cursor.fetchall()
        connection.close()
        return categories

    @staticmethod
    def get_category(category_id):
        connection = Inventory.connect_db()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM categories WHERE id = ?', (category_id,))
        category = cursor.fetchone()
        connection.close()
        return category

    @staticmethod
    def category_exists(category_id):
        connection = Inventory.connect_db()
        cursor = connection.cursor()
        cursor.execute('SELECT 1 FROM categories WHERE id = ?', (category_id,))
        exists = cursor.fetchone() is not None
        connection.close()
        return exists
