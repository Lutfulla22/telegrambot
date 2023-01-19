from telebot import types
from database import Data


# Кнопка для отправки номера
def number_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Сама кнопка
    number = types.KeyboardButton('Отправить номер', request_contact=True)

    # Добвить в пространство
    kb.add(number)

    # Результат нужно вернуть
    return kb


# Кнопка для отправки локации
def location_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Сама кнопка
    location = types.KeyboardButton('Отправить локацию', request_location=True)

    # Добвить в пространство
    kb.add(location)

    # Результат нужно вернуть
    return kb


# Кнопка основного меню
def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Сами кнопки
    katalog = types.KeyboardButton('Каталог')
    call_us = types.KeyboardButton('Связаться с нами')

    # Добавить в пространство
    kb.add(katalog, call_us)

    # Возвращаем результат
    return kb


# Кнопки с продуктами
def catalog_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Сами кнопки берем из базы
    products = Data().show_all_products()
    cart = types.KeyboardButton('Корзина')
    order = types.KeyboardButton('Оформить заказ')
    kb.add(cart, order)

    # Цикл для генерации кнопок
    for i in products:
        # Добавить
        kb.add(types.KeyboardButton(i))

    return kb


# Кнопки для выбора количества
def count_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for i in range(1, 10):
        kb.add(types.KeyboardButton(str(i)))

    return kb


# Кнопки для удаления из корзины
def delete_from_cart_button(user_id):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Сами кнопки берем из базы
    products = Data().show_user_cart(user_id)
    kb.add(types.KeyboardButton('Оформить заказ'), types.KeyboardButton('Очистить корзину'))
    # Цикл для генерации кнопок
    for i in products:
        # Добавить
        kb.add(types.KeyboardButton(f'- {i[1]}'))

    kb.add(types.KeyboardButton('Назад'))
    return kb

