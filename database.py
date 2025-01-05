import sqlite3
from datetime import datetime
connection = sqlite3.connect("data.db")
sql = connection.cursor()

sql.execute("CREATE TABLE IF NOT EXISTS users "
            "(user_id INTEGER, name TEXT, "
            "phone_number TEXT, reg_date DATETIME, language TEXT);")
sql.execute("CREATE TABLE IF NOT EXISTS products "
            "(pr_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "pr_name TEXT, pr_price REAL, pr_desc TEXT,"
            "pr_photo TEXT, pr_quantity INTEGER,"
            "reg_date DATETIME);")
sql.execute("CREATE TABLE IF NOT EXISTS cart "
            "(user_id INTEGER, pr_id INTEGER, "
            "pr_name TEXT, pr_count INTEGER, "
            "total_price REAL);")
connection.commit()
#TODO дз получение айди всех юзеров бота
def get_all_id():
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    sql.execute("SELECT user_id FROM users").fetchall()

def add_user(name, phone_number, user_id, language):
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    sql.execute(f"INSERT INTO users (user_id, name, phone_number, reg_date, language) "
                f"VALUES (?, ?, ?, ?, ?);", (user_id, name, phone_number, datetime.now(), language))
    connection.commit()

def check_user(user_id):
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT * FROM users WHERE user_id=?;", (user_id, )).fetchone()
    if checker:
        return True
    elif not checker:
        return False

def get_all_users():
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    all_users = sql.execute("SELECT * FROM users;").fetchall()
    return all_users

# взаимодействие с продуктами
def add_product(pr_name, pr_price, pr_desc, pr_quantity, pr_photo):
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    sql.execute("INSERT INTO products (pr_name, pr_price, pr_desc, "
                "pr_quantity, pr_photo, reg_date) "
                "VALUES (?, ?, ?, ?, ?, ?);", (pr_name, pr_price, pr_desc,
                                              pr_quantity, pr_photo,
                                              datetime.now()))
    connection.commit()
def get_all_products():
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    all_product = sql.execute("SELECT * FROM products;").fetchall()
    return all_product
def delete_exact_product(pr_id):
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    sql.execute("DELETE FROM products WHERE pr_id = ?;", (pr_id, ))
    connection.commit()
#TODO дз функция изменения количества определенного продукта
def change_quantity(pr_id, new_pr_quantity):
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    sql.execute("UPDATE products SET pr_quantity=? WHERE pr_id =?;",(new_pr_quantity , pr_id))
    connection.commit()

def delete_all_products():
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    sql.execute("DELETE FROM products;")
    connection.commit()

def get_pr_id_name():
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    # берем для кнопок продуктов нужную информацию
    all_product = sql.execute("SELECT pr_id, pr_name, pr_quantity "
                              "FROM products;").fetchall()
    # фильтрация продуктов, оставляем те, что в количестве больше 0
    #[(pr1_id, pr1_name, pr1_quantity), (pr2_id, pr2_name, pr2_quantity), ...]
    actual_products = [[product[0], product[1]] for product
                       in all_product if product[2] > 0]
    # [[pr1_id, pr1_name], [pr2_id,pr2_name]....]
    return actual_products
def get_exact_product(pr_id):
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    product_info = sql.execute("SELECT pr_name, pr_price, pr_desc, pr_photo "
                               "FROM products WHERE pr_id = ?;", (pr_id, )).fetchone()
    return product_info
# работа с корзиной
def add_to_cart(user_id, pr_id, pr_name, pr_price, pr_quantity):
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    total_price = pr_price * pr_quantity
    sql.execute("INSERT INTO cart (user_id, pr_id, pr_name, pr_count, "
                "total_price) VALUES (?, ? ,? ,?, ?);", (user_id, pr_id,
                                                         pr_name, pr_quantity,
                                                         total_price))
    connection.commit()
def delete_user_cart(user_id):
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    sql.execute("DELETE FROM cart WHERE user_id=?;", (user_id, ))
    connection.commit()
#TODO дз получение информации о корзине юзера
# формат информации (название продуктов, количество, общая цена за это количеств)
def get_user_cart(user_id):
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    cart = sql.execute("SELECT pr_name, pr_count, total_price FROM cart WHERE user_id = ?;", (user_id,)).fetchall()
    return cart
def get_cart_id_name(user_id):
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    product = sql.execute("SELECT pr_id, pr_name FROM cart WHERE user_id =?;", (user_id, )).fetchall()
    return product
def delete_exact_product_from_cart(user_id, pr_id):
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    sql.execute('DELETE FROM cart WHERE user_id =? and pr_id=?', (user_id, pr_id))
    connection.commit()

def find_language_db(user_id):
    connection = sqlite3.connect("data.db")
    sql2 = connection.cursor()
    a = sql2.execute("SELECT language FROM users WHERE user_id = ?;", (user_id,)).fetchone()
    return a