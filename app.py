from colorama import Fore, Style
from networkx.algorithms.triads import triad_type
from unicodedata import category

from inventory import Inventory


def add_product():
    name = input("Enter product name: ")
    description = input("Enter product description: ")
    try:
        quantity = int(input("Enter available quantity: "))
    except ValueError:
        print(Fore.RED + "Invalid quantity. Please enter a number." + Style.RESET_ALL)
        add_product()
        return

    try:
        price = float(input("Enter product price: "))
    except ValueError:
        print(Fore.RED + "Invalid price. Please enter a number." + Style.RESET_ALL)
        add_product()
        return
    categories = Inventory.get_categories()
    print(Fore.BLUE + "Product Categories:" + Style.RESET_ALL)
    for category in categories:
        print(f"ID: {category[0]}, Name: {category[1]}")

    try:
        id_category = int(input("Enter the category ID: "))
    except ValueError:
        print(Fore.RED + "Invalid category ID. Please enter a number." + Style.RESET_ALL)
        add_product()
        return
    if not Inventory.category_exists(id_category):
        print(Fore.RED + "Category not found. Please enter a valid category ID." + Style.RESET_ALL)
        add_product()
        return

    Inventory.add_product(name, description, quantity, price, id_category)
    print(Fore.GREEN + "\nProduct successfully added!" + Style.RESET_ALL)


def show_products():
    products = Inventory.get_products()
    print(Fore.BLUE + "\nInventory Products:" + Style.RESET_ALL)
    for product in products:
        category_id = product[5]
        category = Inventory.get_category(category_id)[1]
        print(f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Quantity: {product[3]}, Price: {product[4]}, Category: {category}")


def update_product():
    product_id = int(input("Enter the product ID to update: "))
    if not Inventory.find_product(product_id):
        print(Fore.RED + "\nProduct not found!" + Style.RESET_ALL)
        return
    attribute = input("Enter the attribute to update: ")
    new_value = input("Enter the new value: ")
    Inventory.update_product(product_id, attribute, new_value)
    print(Fore.GREEN + "\nProduct successfully updated!" + Style.RESET_ALL)


def delete_product():
    product_id = int(input("Enter the product ID to delete: "))
    if Inventory.delete_product(product_id):
        print(Fore.GREEN + "\nProduct successfully deleted!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\nProduct not found!" + Style.RESET_ALL)


def find_product():
    product_id = int(input("Enter the product ID to find: "))
    product = Inventory.find_product(product_id)
    if product:
        print(Fore.BLUE + f"\nProduct found: ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Quantity: {product[3]}, Price: {product[4]}, Category: {product[5]}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\nProduct not found!" + Style.RESET_ALL)


def low_stock_report():
    limit = int(input("Enter the low stock limit: "))
    products = Inventory.products_low_stock(limit)
    print(Fore.YELLOW + "\nProducts with low stock:" + Style.RESET_ALL)
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Quantity: {product[3]}, Price: {product[4]}, Category: {product[5]}")

def menu_principal():
    Inventory.initialize_db("inventory.db")
    while True:
        print(Fore.CYAN + "\n--- Main Menu ---" + Style.RESET_ALL)
        print("1. Add product")
        print("2. Show products")
        print("3. Update product")
        print("4. Delete product")
        print("5. Find product")
        print("6. Generate low stock report")
        print("7. Exit")

        option = input("Select an option: ")

        if option == '1':
            add_product()
        elif option == '2':
            show_products()
        elif option == '3':
            update_product()
        elif option == '4':
            delete_product()
        elif option == '5':
            find_product()
        elif option == '6':
            low_stock_report()
        elif option == '7':
            print(Fore.GREEN + "\nThank you for using the application. Goodbye!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "\nInvalid option. Please try again." + Style.RESET_ALL)


if __name__ == '__main__':
    menu_principal()
