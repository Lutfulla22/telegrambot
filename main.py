import telebot
from datetime import datetime

from database import Data
import buttons


# Подключение к боту и к базе
bot = telebot.TeleBot('5876665237:AAFHvWb_r-3-kJ8hICH4_QvMwEZx9HD7Evw')



## Админ панель ##
@bot.message_handler(commands=['admin'])
def admin_message(message):
    admin_id = message.from_user.id

    text = 'Добро пожаловать на панель администратора\nОтправьте название продукта'

    bot.send_message(admin_id, text)

    # Перекинуть на этап получения названия продукта
    bot.register_next_step_handler(message, get_product_name)


# Получение название продукта
def get_product_name(message):
    print(message)
    product_name = message.text

    bot.send_message(message.from_user.id, 'Остаток на складе')

    # Переход на этап получения количества а также перекидка переменной product_name
    bot.register_next_step_handler(message, get_product_amount, product_name)


# Этап получения количества на склад
def get_product_amount(message, product_name):
    product_count = message.text

    bot.send_message(message.from_user.id, 'Цена товара')

    # Переход на этап получения цены а также перекидка product_name, product_amount
    bot.register_next_step_handler(message, get_product_price, product_name, product_count)


# Этап получения цены товара
def get_product_price(message, product_name, product_count):
    product_price = message.text

    bot.send_message(message.from_user.id, 'ОТправьте описание')

    # Переход на этап получения описания а также перекидка product_name, product_count, product_price
    bot.register_next_step_handler(message, get_product_description, product_name, product_count, product_price)


# Этап получения описания товара
def get_product_description(message, product_name ,product_count, product_price):
    product_description = message.text

    bot.send_message(message.from_user.id, 'Отправьте фото для продукта')

    # Переход на этап получения фото а также перекидка product_name, product_count, product_price, product_description
    bot.register_next_step_handler(message, get_product_photo, product_name, product_count, product_price, product_description)


# Этап получения фото, даты
def get_product_photo(message, product_name, product_count, product_price, product_description):
    db = Data()
    if message.photo:

        photo_id = message.photo[0].file_id

        # Сохраняем в базу
        db.add_product(product_name, product_count, product_price, product_description, photo_id, datetime.now())

        bot.send_message(message.from_user.id, 'Продукт успешно добавлен')






# Запуск бота
bot.polling()


