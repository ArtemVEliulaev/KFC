from itertools import product
from telebot import TeleBot
import database as db
import bot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def phone_number_bt(user_id):
    kb = ReplyKeyboardMarkup(resize_keyboard= True)
    language = db.find_language_db(user_id)[0]
    button = KeyboardButton(text = bot.all_text.get("номер_т_кн").get(language),
                            request_contact = True)
    kb.add(button)
    return kb

def location_bt(user_id):
    language = db.find_language_db(user_id)[0]
    kb = ReplyKeyboardMarkup(resize_keyboard= True)
    button = KeyboardButton(text = bot.all_text.get("локация_кн").get(language),
                            request_location = True)
    kb.add(button)
    return kb

def languages_in():
    kb = InlineKeyboardMarkup(row_width =2)
    ru = InlineKeyboardButton(text = "RU", callback_data = "RU")
    uz = InlineKeyboardButton(text = "UZ", callback_data = "UZ")
    kb.add(ru,uz)
    return kb

def main_menu_bt(user_id):
    language = db.find_language_db(user_id)[0]
    kb = ReplyKeyboardMarkup(resize_keyboard= True)
    button1 = KeyboardButton(text=bot.all_text.get("меню").get(language))
    button2 = KeyboardButton(text=bot.all_text.get("отзыв_кн").get(language))
    button3 = KeyboardButton(text=bot.all_text.get("корзина_кн").get(language))
    kb.row(button1)
    kb.row(button2,button3)
    return kb

def product_in(all_products,user_id):
    kb = InlineKeyboardMarkup(row_width =2)
    #статичные
    language = db.find_language_db(user_id)[0]
    back = InlineKeyboardButton(text = bot.all_text.get("назад_кн").get(language), callback_data= "back")
    cart = InlineKeyboardButton(text = bot.all_text.get("корзина").get(language), callback_data= "cart")
    #Динамичные
    buttons = [InlineKeyboardButton(text= f"{product[1]}", callback_data =f"prod_{product[0]}")
               for product in all_products]
    kb.add(*buttons)
    kb.row(cart)
    kb.row(back)
    return kb

def plus_or_minus_in(user_id, plus_or_minus="", current_amount = 1):
    kb = InlineKeyboardMarkup(row_width=3)
    language = db.find_language_db(user_id)[0]
    back = InlineKeyboardButton(text = bot.all_text.get("назад_кн").get(language), callback_data = "back_product")
    to_cart = InlineKeyboardButton( text = bot.all_text.get("доб_в_кор").get(language), callback_data = "to_cart")
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

def cart_in(cart,user_id):
    kb = InlineKeyboardMarkup(row_width=1)
    language = db.find_language_db(user_id)[0]
    clear = InlineKeyboardButton(text =bot.all_text.get("очистить_к").get(language) , callback_data = "clear_cart")
    order = InlineKeyboardButton(text=bot.all_text.get("оформить_з").get(language), callback_data="order")
    back = InlineKeyboardButton(text=bot.all_text.get("назад_кн").get(language), callback_data="back_product")
    kb.add(order, clear, back)
    if cart:
        products = [InlineKeyboardButton(text = f"❌ {product[1]}", callback_data = f"delete_{product[0]}") for product in cart]
        kb.add(*products)

    return kb
