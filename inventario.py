import sqlite3

class Inventario:
    @staticmethod
    def conectar_db():
        return sqlite3.connect('inventario.db')

    @staticmethod
    def inicializar_db():
        conexion = Inventario.conectar_db()
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT
            )
        ''')
        conexion.commit()
        conexion.close()

    @staticmethod
    def registrar_producto(nombre, descripcion, cantidad, precio, categoria):
        conexion = Inventario.conectar_db()
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, descripcion, cantidad, precio, categoria))
        conexion.commit()
        conexion.close()

    @staticmethod
    def obtener_productos():
        conexion = Inventario.conectar_db()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        conexion.close()
        return productos

    @staticmethod
    def actualizar_producto(id_producto, nueva_cantidad):
        conexion = Inventario.conectar_db()
        cursor = conexion.cursor()
        cursor.execute('''
            UPDATE productos
            SET cantidad = ?
            WHERE id = ?
        ''', (nueva_cantidad, id_producto))
        cambios = cursor.rowcount
        conexion.commit()
        conexion.close()
        return cambios > 0

    @staticmethod
    def eliminar_producto(id_producto):
        conexion = Inventario.conectar_db()
        cursor = conexion.cursor()
        cursor.execute('''
            DELETE FROM productos
            WHERE id = ?
        ''', (id_producto,))
        cambios = cursor.rowcount
        conexion.commit()
        conexion.close()
        return cambios > 0

    @staticmethod
    def buscar_producto(id_producto):
        conexion = Inventario.conectar_db()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM productos WHERE id = ?', (id_producto,))
        producto = cursor.fetchone()
        conexion.close()
        return producto

    @staticmethod
    def productos_bajo_stock(limite):
        conexion = Inventario.conectar_db()
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM productos WHERE cantidad <= ?', (limite,))
        productos = cursor.fetchall()
        conexion.close()
        return productos
