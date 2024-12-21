import json
import os
import sys
from sqlite3 import IntegrityError

from colorama import Fore, Style

from inventory import Inventory

current_language = "en"
translations = {}

def load_translations(language):
    global translations
    try:
        with open(f"translations/{language}.json", "r", encoding="utf-8") as file:
            translations = json.load(file)
    except FileNotFoundError:
        print(f"Error: Translation file for '{language}' not found.")
        sys.exit(1)

def _(key):
    return translations.get(key, key)

def change_language():
    global current_language
    print("1. English")
    print("2. Español")
    option = input(_('select_language'))
    if option == '1':
        current_language = "en"
    elif option == '2':
        current_language = "es"
    else:
        print(Fore.RED + _("invalid_option") + Style.RESET_ALL)
        return
    load_translations(current_language)
    print(Fore.GREEN + _("language_changed_successfully") + Style.RESET_ALL)

def show_products_table_header():
    print("+------+----------------------+----------------------+----------+-------------+-------------------+")
    print(f"| {'ID':^4} | {_('name'):^20} | {_('description'):^20} | {_('quantity'):^8} | {_('price'):^11} | {_('category'):^17} |")
    print("+------+----------------------+----------------------+----------+-------------+-------------------+")

def product_to_table_row(producto):
    category = _(producto[5]) if producto[5] in translations else producto[5]
    return f"| {producto[0]:^4} | {producto[1][:20]:^20} | {producto[2][:20]:^20} | {producto[3]:^8} | ${producto[4]:^10.2f} | {category[:17]:^17} |"

def end_products_table():
    print("+------+----------------------+----------------------+----------+-------------+-------------------+")

def show_product_categories():
    categories = Inventory.get_categories()
    print(Fore.BLUE + _("product_categories") + Style.RESET_ALL)
    for category in categories:
        print(f"ID: {category[0]}, {_('name')}: {_(category[1]) if category[1] in translations else category[1]}")

def add_product():
    name = input(_("enter_product_name"))
    description = input(_("enter_product_description"))
    try:
        quantity = int(input(_("enter_product_quantity")))
    except ValueError:
        print(Fore.RED + _("invalid_quantity") + Style.RESET_ALL)
        return add_product()
    if quantity < 0:
        print(Fore.RED + _("invalid_quantity") + Style.RESET_ALL)
        return add_product()

    try:
        price = float(input(_("enter_product_price")))
    except ValueError:
        print(Fore.RED + _("invalid_price") + Style.RESET_ALL)
        return add_product()
    if price <= 0:
        print(Fore.RED + _("invalid_price") + Style.RESET_ALL)
        return add_product()

    show_product_categories()

    try:
        id_category = int(input(_("enter_category_id")))
    except ValueError:
        print(Fore.RED + _("invalid_category_id") + Style.RESET_ALL)
        return add_product()
    if not Inventory.category_exists(id_category):
        print(Fore.RED + _("category_not_found") + Style.RESET_ALL)
        return add_product()

    Inventory.add_product(name, description, quantity, price, id_category)
    print(Fore.GREEN + "\n" + _("product_added_successfully") + Style.RESET_ALL)


def show_products(products):
    if not products:
        print(Fore.RED + _("no_products_yet") + Style.RESET_ALL)
        return
    show_products_table_header()
    for product in products:
        print(product_to_table_row(product))
    end_products_table()

def show_product(product):
    show_products_table_header()
    print(product_to_table_row(product))
    end_products_table()

def update_product():
    try:
        product_id = int(input(_("enter_product_id")))
    except ValueError:
        print(Fore.RED + "\n" + _("invalid_product_id") + Style.RESET_ALL)
        return update_product()
    if not Inventory.find_product_by_id(product_id):
        print(Fore.RED + "\n" + _("product_not_found") + Style.RESET_ALL)
        return

    product = Inventory.find_product_by_id(product_id)
    print(Fore.BLUE + f"\n" + _("product_found") + Style.RESET_ALL)
    show_product(product)

    columns = Inventory.get_table_columns("products")
    attributes_names = ["name", "description", "quantity", "price", "id_category"]
    print(_("update_product_attributes"))
    print("1. " + _("name"))
    print("2. " + _("description"))
    print("3. " + _("quantity"))
    print("4. " + _("price"))
    print("5. " + _("category"))

    try:
        attribute_number = int(input(_("enter_attribute_to_update")))
    except ValueError:
        print(Fore.RED + "\n" + _("invalid_attribute") + Style.RESET_ALL)
        return update_product()

    if attribute_number < 1 or attribute_number > 5:
        print(Fore.RED + "\n" + _("invalid_attribute") + Style.RESET_ALL)
        return update_product()

    attribute = attributes_names[attribute_number - 1]

    column_type = None
    for column in columns:
        if column["name"] == attribute:
            column_type = column["type"]
            break

    if attribute == "id_category":
        show_product_categories()

    new_value = input(_("enter_new_value"))

    if column_type == "INTEGER":
        try:
            new_value = int(new_value)
        except ValueError:
            print(Fore.RED + "\n" + _("invalid_value_integer") + Style.RESET_ALL)
            return update_product()
        if attribute == "quantity" and new_value < 0:
            print(Fore.RED + "\n " + _("invalid_quantity") + Style.RESET_ALL)
            return update_product()
    elif column_type == "REAL":
        try:
            new_value = float(new_value)
        except ValueError:
            print(Fore.RED + "\n" + _("invalid_value_float") + Style.RESET_ALL)
            return update_product()
        if attribute == "price" and new_value <= 0:
            print(Fore.RED + "\n" + _("invalid_price") + Style.RESET_ALL)
            return update_product()

    if attribute == "id_category" and not Inventory.category_exists(new_value):
        print(Fore.RED + "\n" + _("category_not_found") + Style.RESET_ALL)
        return update_product()

    success = Inventory.update_product(product_id, attribute, new_value)
    if success:
        print(Fore.GREEN + "\n" + _("product_updated_successfully") + Style.RESET_ALL)
    else:
        print(Fore.RED + "\n" + _("product_not_updated") + Style.RESET_ALL)


def delete_product():
    try:
        product_id = int(input(_("enter_product_id")))
    except ValueError:
        print(Fore.RED + "\n" + _("invalid_product_id") + Style.RESET_ALL)
        return delete_product()
    
    product = Inventory.find_product_by_id(product_id)
    if not product:
        print(Fore.RED + "\n" + _("product_not_found") + Style.RESET_ALL)
        return
    
    print(Fore.BLUE + f"\n" + _("product_found") + Style.RESET_ALL)
    show_product(product)

    confirmation = input(_("delete_confirmation"))
    if confirmation.lower() != "y":
        return

    if Inventory.delete_product(product_id):
        print(Fore.GREEN + "\n" + _("product_deleted_successfully") + Style.RESET_ALL)
    else:
        print(Fore.RED + "\n" + _("product_not_found") + Style.RESET_ALL)


def find_products():
    print(Fore.BLUE + "\n" + _("find_products_by") + Style.RESET_ALL)
    print("1. ID")
    print("2. " + _("name"))
    print("3. " + _("category"))

    try:
        option = int(input(_("select_option")))
    except ValueError:
        print(Fore.RED + _("invalid_option") + Style.RESET_ALL)
        find_products()
        return

    product = None

    if option == 1:
        try:
            product_id = int(input(_("enter_product_id")))
        except ValueError:
            print(Fore.RED + _("invalid_product_id") + Style.RESET_ALL)
            return find_products()
        product = Inventory.find_product_by_id(product_id)

    elif option == 2:
        product_name = input(_("enter_product_name"))
        product = Inventory.find_product_by_name(product_name)

    elif option == 3:
        show_product_categories()
        try:
            category_id = int(input(_("enter_category_id")))
        except ValueError:
            print(Fore.RED + _("invalid_category_id") + Style.RESET_ALL)
            return find_products()

        products = Inventory.find_products_by_category(category_id)
        if products:
            print(Fore.BLUE + "\n" + _("products_in_category") + Style.RESET_ALL)
            show_products(products)
        else:
            print(Fore.RED + "\n" + _("no_products_in_category") + Style.RESET_ALL)
        return

    if product:
        print(Fore.BLUE + f"\n" + _("product_found") + Style.RESET_ALL)
        show_product(product)
    else:
        print(Fore.RED + "\n" + _("product_not_found") + Style.RESET_ALL)


def low_stock_report():
    try:
        limit = int(input(_("enter_limit")))
    except ValueError:
        print(Fore.RED + _("invalid_limit") + Style.RESET_ALL)
        low_stock_report()
        return
    products = Inventory.products_low_stock(limit)
    print(Fore.YELLOW + "\n" + _("low_stock_report_generated") + Style.RESET_ALL)
    if not products:
        print(Fore.RED + _("no_products_low_stock") + Style.RESET_ALL)
        return
    show_products(products)


def clear_screen():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/Mac
        os.system('clear')


def main():
    Inventory.initialize_db("inventory.db")
    load_translations(current_language)  # Cargar traducciones iniciales
    while True:
        print("+" + "-" * 50 + "+")
        print(f"|{_('main_menu'):^50}|")
        print("+" + "-" * 50 + "+")
        print(f"| 1. {_('add_product'):<45} |")
        print(f"| 2. {_('show_products'):<45} |")
        print(f"| 3. {_('update_product'):<45} |")
        print(f"| 4. {_('delete_product'):<45} |")
        print(f"| 5. {_('find_products'):<45} |")
        print(f"| 6. {_('low_stock_report'):<45} |")
        print(f"| 7. {_('change_language'):<45} |")  
        print(f"| 8. {_('exit'):<45} |")
        print("+" + "-" * 50 + "+")

        option = input(_("select_option"))
        if option == '1':
            add_product()
        elif option == '2':
            print(Fore.BLUE + "\n" + _("inventory_products") + Style.RESET_ALL)
            show_products(Inventory.get_products())
        elif option == '3':
            update_product()
        elif option == '4':
            delete_product()
        elif option == '5':
            find_products()
        elif option == '6':
            low_stock_report()
        elif option == '7':
            change_language()
        elif option == '8':
            print(Fore.GREEN + _("thank_you") + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + _("invalid_option") + Style.RESET_ALL)
        input("\n" + _('press_enter') + "\n")
        clear_screen()



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\n' + Fore.RED + _("keyboard_interrupt") + Style.RESET_ALL)
        try:
            sys.exit(130)
        except SystemExit:
            sys.exit(0)

