from itertools import product

all_text = {""}
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
def phone_number_db():
    kb = ReplyKeyboardMarkup(resize_keyboard= True)

    button = KeyboardButton(text = "📞Поделиться номером телефона📞",
                            request_contact = True)
    kb.add(button)
    return kb

def location_bt():
    kb = ReplyKeyboardMarkup(resize_keyboard= True)
    button = KeyboardButton(text = "🗺Поделиться локацией🗺",
                            request_location = True)
    kb.add(button)
    return kb

def languages_in():
    kb = InlineKeyboardMarkup(row_width =2)
    ru = InlineKeyboardButton(text = "RU", callback_data = "RU")
    uz = InlineKeyboardButton(text = "UZ", callback_data = "UZ")
    kb.add(ru,uz)
    return kb
def main_menu_bt():
    kb = ReplyKeyboardMarkup(resize_keyboard= True)
    button1 = KeyboardButton(text="🍴Меню🍴")
    button2 = KeyboardButton(text="✍️Отзыв✍️")
    button3 = KeyboardButton(text="🛒Корзина🛒")
    kb.row(button1)
    kb.row(button2,button3)
    return kb
def product_in(all_products):
    kb = InlineKeyboardMarkup(row_width =2)
    #статичные
    back = InlineKeyboardButton(text = "Назад", callback_data= "back")
    cart = InlineKeyboardButton(text = "Корзина", callback_data= "cart")
    #Динамичные
    buttons = [InlineKeyboardButton(text= f"{product[1]}", callback_data =f"prod_{product[0]}")
               for product in all_products]
    kb.add(*buttons)
    kb.row(cart)
    kb.row(back)
    return kb
def plus_or_minus_in(plus_or_minus="", current_amount = 1):
    kb = InlineKeyboardMarkup(row_width=3)
    back = InlineKeyboardButton(text = "Назад", callback_data = "back_product")
    to_cart = InlineKeyboardButton( text = "Добавить в корзиину", callback_data = "to_cart")
    minus = InlineKeyboardButton( text = "-", callback_data = "minus")
    plus = InlineKeyboardButton(text = "+", callback_data = "plus")
    count = InlineKeyboardButton(text = f"{current_amount}", callback_data = "none")
    if plus_or_minus == "plus":
        count = InlineKeyboardButton(text = f"{current_amount +1}", callback_data= "none")
    elif plus_or_minus == "minus":
        if current_amount >1:
            count = InlineKeyboardButton(text = f"{current_amount -1}", callback_data = "none")
    kb.row(minus,count, plus)
    kb.row(to_cart)
    kb.row(back)
    return kb
def cart_in(cart):
    kb = InlineKeyboardMarkup(row_width=1)
    clear = InlineKeyboardButton(text = "Очистить корзину", callback_data = "clear_cart")
    order = InlineKeyboardButton(text="Оформить заказ", callback_data="order")
    back = InlineKeyboardButton(text="Назад", callback_data="back_product")
    kb.add(order, clear, back)
    if cart:
        products = [InlineKeyboardButton(text = f"❌ {product[1]}", callback_data = f"delete_{product[0]}") for product in cart]
        kb.add(*products)

    return kb