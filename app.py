import os
import sys

from colorama import Fore, Style


from inventory import Inventory

def show_product_categories():
    categories = Inventory.get_categories()
    print(Fore.BLUE + "Product Categories:" + Style.RESET_ALL)
    for category in categories:
        print(f"ID: {category[0]}, Name: {category[1]}")

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

    show_product_categories()

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
    if not products:
        print(Fore.RED + "No products yet!" + Style.RESET_ALL)
        return
    for product in products:
        category = Inventory.get_category(product[5])[1]
        print(f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Quantity: {product[3]}, Price: {product[4]}, Category: {category}")


def update_product():
    product_id = int(input("Enter the product ID to update: "))
    if not Inventory.find_product_by_id(product_id):
        print(Fore.RED + "\nProduct not found!" + Style.RESET_ALL)
        return

    product = Inventory.find_product_by_id(product_id)
    category = Inventory.get_category(product[5])[1]
    print(Fore.BLUE + f"\nProduct found: ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Quantity: {product[3]}, Price: {product[4]}, Category: {category}" + Style.RESET_ALL)

    columns = Inventory.get_table_columns("products")
    attributes_names = ["name", "description", "quantity", "price", "id_category"]
    print("Available attributes to update:")
    print("1. Name")
    print("2. Description")
    print("3. Quantity")
    print("4. Price")
    print("5. Category")

    try:
        attribute_number = int(input("Enter the attribute number to update: "))
    except ValueError:
        print(Fore.RED + "\nInvalid attribute number. Please enter a number." + Style.RESET_ALL)
        return update_product()

    if attribute_number < 1 or attribute_number > 5:
        print(Fore.RED + "\nInvalid attribute number. Please try again." + Style.RESET_ALL)
        return update_product()

    attribute = attributes_names[attribute_number - 1]

    column_type = None
    for column in columns:
        if column["name"] == attribute:
            column_type = column["type"]
            break

    if attribute == "id_category":
        show_product_categories()

    new_value = input("Enter the new value: ")

    if column_type == "INTEGER":
        try:
            new_value = int(new_value)
        except ValueError:
            print(Fore.RED + "\nInvalid value. Expected an integer." + Style.RESET_ALL)
            return update_product()
    elif column_type == "REAL":
        try:
            new_value = float(new_value)
        except ValueError:
            print(Fore.RED + "\nInvalid value. Expected a decimal number." + Style.RESET_ALL)
            return update_product()

    if attribute == "id_category" and not Inventory.category_exists(new_value):
        print(Fore.RED + "\nCategory not found. Please enter a valid category ID." + Style.RESET_ALL)
        return update_product()

    success = Inventory.update_product(product_id, attribute, new_value)
    if success:
        print(Fore.GREEN + "\nProduct successfully updated!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\nFailed to update the product." + Style.RESET_ALL)


def delete_product():
    try:
        product_id = int(input("Enter the product ID to delete: "))
    except ValueError:
        print(Fore.RED + "Invalid product ID. Please enter a number." + Style.RESET_ALL)
        return delete_product()
    if Inventory.delete_product(product_id):
        print(Fore.GREEN + "\nProduct successfully deleted!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\nProduct not found!" + Style.RESET_ALL)


def find_products():
    print(Fore.BLUE + "\nFind Products by:" + Style.RESET_ALL)
    print("1. ID")
    print("2. Name")
    print("3. Category")

    try:
        option = int(input("Select an option: "))
    except ValueError:
        print(Fore.RED + "Invalid option. Please enter a number." + Style.RESET_ALL)
        find_products()
        return

    product = None

    if option == 1:
        try:
            product_id = int(input("Enter the product ID: "))
        except ValueError:
            print(Fore.RED + "Invalid product ID. Please enter a number." + Style.RESET_ALL)
            find_products()
            return
        product = Inventory.find_product_by_id(product_id)

    elif option == 2:
        product_name = input("Enter the product name: ")
        product = Inventory.find_product_by_name(product_name)

    elif option == 3:
        show_product_categories()
        try:
            category_id = int(input("Enter the category ID: "))
        except ValueError:
            print(Fore.RED + "Invalid category ID. Please enter a number." + Style.RESET_ALL)
            find_products()
            return

        products = Inventory.find_products_by_category(category_id)
        if products:
            print(Fore.BLUE + "\nProducts in Category:" + Style.RESET_ALL)
            for product in products:
                print(f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Quantity: {product[3]}, Price: {product[4]}")
        else:
            print(Fore.RED + "No products found in this category!" + Style.RESET_ALL)
        return

    if product:
        print(Fore.BLUE + f"\nProduct found: ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Quantity: {product[3]}, Price: {product[4]}, Category: {product[5]}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\nProduct not found!" + Style.RESET_ALL)


def low_stock_report():
    try:
        limit = int(input("Enter the low stock limit: "))
    except ValueError:
        print(Fore.RED + "Invalid limit. Please enter a number." + Style.RESET_ALL)
        low_stock_report()
        return
    products = Inventory.products_low_stock(limit)
    print(Fore.YELLOW + "\nProducts with low stock:" + Style.RESET_ALL)
    if not products:
        print(Fore.RED + "No products with low stock!" + Style.RESET_ALL)
        return
    for product in products:
        print(f"ID: {product[0]}, Name: {product[1]}, Description: {product[2]}, Quantity: {product[3]}, Price: {product[4]}, Category: {product[5]}")


def clear_screen():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/Mac
        os.system('clear')


def main():
    Inventory.initialize_db("inventory.db")
    while True:
        print("+" + "-" * 50 + "+")
        print(f"|{' Main Menu ':^50}|")
        print("+" + "-" * 50 + "+")
        print(f"| {'1. Add product':<48} |")
        print(f"| {'2. Show products':<48} |")
        print(f"| {'3. Update product':<48} |")
        print(f"| {'4. Delete product':<48} |")
        print(f"| {'5. Find products':<48} |")
        print(f"| {'6. Generate low stock report':<48} |")
        print(f"| {'7. Exit':<48} |")
        print("+" + "-" * 50 + "+")

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
            find_products()
        elif option == '6':
            low_stock_report()
        elif option == '7':
            print(Fore.GREEN + "\nThank you for using the application. Goodbye!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "\nInvalid option. Please try again." + Style.RESET_ALL)
        input("\nPress Enter to continue...")

        clear_screen()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(130)
        except SystemExit:
            sys.exit(0)

