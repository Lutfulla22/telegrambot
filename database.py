import sqlite3


## Создаем подключение и переводчика ##
connection = sqlite3.connect('dostavka.db')
sql = connection.cursor()

## Создаем таблицы ##
# Пользователи
sql.execute('CREATE TABLE IF NOT EXISTS users '
            '(user_id INTEGER,'
            'name TEXT,'
            'number TEXT, '
            'address TEXT,'
            'reg_date DATETIME);')

# Продукты
sql.execute('CREATE TABLE IF NOT EXISTS products '
            '(pr_id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'pr_name TEXT, '
            'pr_amount INTEGER, '
            'pr_price REAL, '
            'pr_des TEXT, '
            'pr_photo TEXT,'
            'pr_add_date DATETIME);')

# Корзина поль-я
sql.execute('CREATE TABLE IF NOT EXISTS user_cart '
            '(user_id INTEGER, '
            'user_product TEXT, '
            'pr_quantity INTEGER, '
            'total REAL);')

# Заказы
sql.execute('CREATE TABLE IF NOT EXISTS orders '
            '(id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'user_id INTEGER, '
            'user_address TEXT, '
            'payment TEXT, '
            'total_cost REAL, '
            'order_date DATETIME);')



## Класс для взаимодействия с Базой данных ##
class Data:
    def __init__(self):
        self.connection = sqlite3.connect('dostavka.db')
        self.sql = self.connection.cursor()

    ## Методы для пользователя ##
    # Регистрация
    def registration(self, user_id, name, number, address, reg_date):
        self.sql.execute('INSERT INTO users VALUES (?,?,?,?,?);', (user_id, name, number, address, reg_date))

        # Фиксируем обновления
        self.connection.commit()

    # Проверка на наличие user_id в базе
    def check_user(self, user_id):
        checker = self.sql.execute('SELECT user_id FROM users WHERE user_id=?;', (user_id,))

        if checker.fetchone():
            return True

        else:
            return False

    # Добавление в корзину
    def add_to_cart(self, user_id, user_product, pr_quantity):
        # Получаем цену продукта который выборал пользователь
        current_product = self.sql.execute('SELECT pr_price FROM products WHERE pr_name=?', (user_product,)).fetchone()

        # Считаем стоимость
        total = current_product[0]*pr_quantity

        # Заносим в базу
        self.sql.execute('INSERT INTO user_cart VALUES (?,?,?,?);', (user_id, user_product, pr_quantity, total))

        # Зафиксировать обновления
        self.connection.commit()

    # Отображение корзины
    def show_user_cart(self, user_id):
        user_cart = self.sql.execute('SELECT * FROM user_cart WHERE user_id=?;', (user_id,)).fetchall()

        return user_cart

    # Удаление из корзины
    def delete_product_from_cart(self, product_name, user_id):
        self.sql.execute('DELETE FROM user_cart WHERE user_product=? AND user_id=?;', (product_name, user_id))

        self.connection.commit()

    # Очистка корзины пользователя
    def clear_user_cart(self, user_id):
        self.sql.execute('DELETE FROM user_cart WHERE user_id=?;', (user_id,))

        self.connection.commit()

    # Оформление заказа
    def confirm_order(self, user_id, user_address, payment, order_date):
        user_cart = self.sql.execute('SELECT total FROM user_cart WHERE user_id=?;', (user_id,)).fetchall()

        total_cost = sum([i[0] for i in user_cart])

        # Заносим в таблицу
        self.sql.execute('INSERT INTO orders '
                         '(user_id, user_address, payment, total_cost, order_date) VALUES (?,?,?,?,?);',
                         (user_id, user_address, payment, total_cost, order_date))

        # Зафиксировать обновления
        self.connection.commit()

    ## Работа с продуктами ##
    ##### ДЗ #####
    # Получить все названия продуктов
    def show_all_products(self):
        all_products = self.sql.execute('SELECT pr_name FROM products;').fetchall()

        return [i[0] for i in all_products]

    # Информация о конкретном продукте
    def get_current_product(self, product_name):
        current_product = self.sql.execute('SELECT pr_name, pr_price, pr_des, pr_photo '
                                           'FROM products WHERE pr_name=?;', (product_name,)).fetchone()

        return current_product

    ## Админ часть ##
    # Добавление продуктов
    def add_product(self, pr_name, pr_count, pr_price, pr_des, pr_photo, added_date):
        self.sql.execute('INSERT INTO products '
                         '(pr_name, pr_amount, pr_price, pr_des, pr_photo, pr_add_date) VALUES (?,?,?,?,?,?);',
                         (pr_name, pr_count, pr_price, pr_des, pr_photo, added_date))

        # Зафиксировать
        self.connection.commit()

