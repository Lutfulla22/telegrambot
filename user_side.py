import telebot
from geopy.geocoders import Nominatim
from datetime import datetime

from database import Data
import buttons

bot = telebot.TeleBot('5876665237:AAFHvWb_r-3-kJ8hICH4_QvMwEZx9HD7Evw')
geolocator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                  '(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    checker = Data().check_user(user_id)
    if checker:
        text = 'Выберите пункт меню'
        bot.send_message(user_id, text, reply_markup=buttons.main_menu())
    else:
        text = 'Добро пожаловать\nОтправьте свое имя'
        bot.send_message(user_id, text)

        bot.register_next_step_handler(message, get_names)

# Этап получения имени
def get_names(message):
    username = message.text

    bot.send_message(message.from_user.id, 'Отправьте свой номер', reply_markup=buttons.number_button())

    bot.register_next_step_handler(message, get_number, username)

def get_number(message, username):
    user_id = message.from_user.id

    if message.contact:
        user_number = message.contact.phone_number

        bot.send_message(user_id, 'Oтправьте свою локацию', reply_markup=buttons.location_button())

        bot.register_next_step_handler(message, get_location, username, user_number)
    else:
        bot.send_message(user_id, 'Отправьте номер с помощью кнопки')
        bot.register_next_step_handler(message, get_number, username)

def get_location(message, username, user_number):
    user_id = message.from_user.id

    if message.location:

        user_adress = geolocator.reverse(f'{message.location.latitude}, {message.location.longitude}')
        Data().registration(user_id, username, user_number, str(user_adress.address), datetime.now())
        bot.send_message(user_id, 'Успешно зарегестрирован\nВыберите пункт меню', reply_markup=buttons.main_menu())

    else:
        bot.send_message(user_id, 'Отправьте локацию с помошью кнопки')
        bot.register_next_step_handler(message, get_location, username, user_number)

@bot.message_handler(content_types=['text'])
def text_message(message):
    user_id = message.from_user.id

    if message.text == 'Каталог':
        text = 'Выберите продукт'

        bot.send_message(user_id, text, reply_markup=buttons.catalog_button())

    elif message.text == "Связаться с нами":
        text = 'Наш номер: +998994884317'
        bot.send_message(user_id, text)

    elif message.text in Data().show_all_products():
        about_product = Data().get_current_product(message.text)
        bot.send_message(user_id, f'{about_product[0]}\nЦеня: {about_product[1]}\nОписание: {about_product[2]}\n\n'
                                  f'Выберите количество:', reply_markup=buttons.count_button())

        bot.register_next_step_handler(message, get_pr_count, message.text)
    elif message.text == 'Корзина':
        user_cart = Data().show_user_cart(user_id)
        text = 'Ваша корзина'
        for i in user_cart:
            text = f'{i[1]} : {i[2]} = {i[3]}\n'
        bot.send_message(user_id, text, reply_markup=buttons.delete_from_cart_button(user_id))

        bot.register_next_step_handler(message, work_with_cart)

def work_with_cart(message):
    user_id = message.from_user.id

    if message.text == 'Назад':
        bot.send_message(user_id, 'Выберите продукт', reply_markup=buttons.catalog_button())

    elif message.text.startswith('-'):
        Data.delete_product_from_cart(message.text[2:], user_id)

        bot.send_message(user_id, 'Продукт удален из корзины', reply_markup=buttons.catalog_button())
    elif message.text == 'Оформить заказ':
        pass

    elif message.text == 'Очистить корзину':
        Data().clear_user_cart(user_id)

        bot.send_message(user_id, 'Корзины очищена', reply_markup=buttons.catalog_button())

def get_pr_count(message, product):
    user_id = message.from_user.id
    product_count = message.text
    if product_count.isnumeric:
        text = 'Продукт успешно добавлен'

        Data().add_to_cart(user_id, product, int(product_count))
        bot.send_message(user_id, text, reply_markup=buttons.catalog_button())

    else:
        text = 'Выберите количество использую цифры'

        bot.send_message(user_id, text)

        bot.register_next_step_handler(message, get_pr_count, product)

bot.polling()