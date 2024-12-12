from colorama import Fore, Style
from inventory import Inventory


def registrar_producto():
    nombre = input("Ingrese el nombre del producto: ")
    descripcion = input("Ingrese la descripcion del producto: ")
    cantidad = int(input("Ingrese la cantidad disponible: "))
    precio = float(input("Ingrese el precio del producto: "))
    categoria = input("Ingrese la categoria del producto: ")
    Inventory.add_product(nombre, descripcion, cantidad, precio, categoria)
    print(Fore.GREEN + "\nProducto registrado exitosamente!" + Style.RESET_ALL)


def mostrar_productos():
    productos = Inventory.get_products()
    print(Fore.BLUE + "\nProductos en el inventario:" + Style.RESET_ALL)
    for producto in productos:
        print(
            f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: {producto[4]}, Categoría: {producto[5]}")


def actualizar_producto():
    id_producto = int(input("Ingrese el ID del producto a actualizar: "))
    nueva_cantidad = int(input("Ingrese la nueva cantidad: "))
    if Inventory.update_product(id_producto, nueva_cantidad):
        print(Fore.GREEN + "\nProducto actualizado exitosamente!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\nProducto no encontrado!" + Style.RESET_ALL)


def eliminar_producto():
    id_producto = int(input("Ingrese el ID del producto a eliminar: "))
    if Inventory.delete_product(id_producto):
        print(Fore.GREEN + "\nProducto eliminado exitosamente!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\nProducto no encontrado!" + Style.RESET_ALL)


def buscar_producto():
    id_producto = int(input("Ingrese el ID del producto a buscar: "))
    producto = Inventory.find_product(id_producto)
    if producto:
        print(
            Fore.BLUE + f"\nProducto encontrado: ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: {producto[4]}, Categoría: {producto[5]}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\nProducto no encontrado!" + Style.RESET_ALL)


def reporte_bajo_stock():
    limite = int(input("Ingrese el límite de bajo stock: "))
    productos = Inventory.products_low_stock(limite)
    print(Fore.YELLOW + "\nProductos con bajo stock:" + Style.RESET_ALL)
    for producto in productos:
        print(
            f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: {producto[4]}, Categoría: {producto[5]}")


def menu_principal():
    Inventory.initialize_db()
    while True:
        print(Fore.CYAN + "\n--- Menú Principal ---" + Style.RESET_ALL)
        print("1. Registrar producto")
        print("2. Mostrar productos")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Buscar producto")
        print("6. Generar reporte de bajo stock")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            registrar_producto()
        elif opcion == '2':
            mostrar_productos()
        elif opcion == '3':
            actualizar_producto()
        elif opcion == '4':
            eliminar_producto()
        elif opcion == '5':
            buscar_producto()
        elif opcion == '6':
            reporte_bajo_stock()
        elif opcion == '7':
            print(Fore.GREEN + "\nGracias por usar la aplicación. Adiós!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "\nOpción no válida. Intente nuevamente." + Style.RESET_ALL)


if __name__ == '__main__':
    menu_principal()
