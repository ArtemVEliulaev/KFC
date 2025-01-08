from telebot import TeleBot
import bot_buttons as bt
from geopy import Photon
import database as db
import translate as tr
from bot_buttons import main_menu_bt

admins_group = -4661710704
geolocator = Photon(user_agent="geo_locator", timeout=10)

# db.add_product("Гамбургер", 30000.00, "Сочный, аппетитный бургер с нежной котлетой, свежими овощами и тягучим сыром, обёрнутый в мягкую булочку", 5, "https://kfc.com.uz/admin/files/medium/medium_4473.jpg")
# db.add_product("Чизбургер", 35000.00, "Тёплый чизбургер с расплавленным сыром, идеально сочетающимся с ароматной котлетой и свежими овощами в мягкой булочке.", 29, "https://kfs-menu.ru/images/menu/chizburger_mini.jpg")
# db.add_product("Хотдог", 28000.00, "Сочная сосиска в мягкой булочке, дополненная нежными соусами и свежими овощами", 23, "https://topkuponi.com/image/cache/catalog/photo/707911285-longer-600x600.jpg")
# db.add_product("Боксмастер", 22000.00, "Боксмастер — это нежный лаваш, наполненный свежими овощами, соусами и вкусными начинками, создающими идеальное сочетание", 9, "https://kfc-burgers.ru/wp-content/uploads/2018/11/BoksMaster-CHizz-Bekon.jpg")
# db.add_product("Донат", 19000.00, "Клубничный пончик с мягким тестом и насыщенной сладкой начинкой, дарящий яркий ягодный вкус в каждом укусе.", 30, "https://kfs-menu.ru/images/menu/donat-klubnichnyy_mini.jpg")
# db.add_product("Шефбургер", 41000.00, "Шефбургер — сочная котлета, свежие овощи и пикантные соусы, объединённые в идеальный вкус в мягкой булочке.", 30, "https://kfs-menu.ru/images/menu/shefburger_mini.jpg")
# db.add_product("Лонгер", 29000.00, "Лонгер — длинная булочка с мягкой текстурой, в которой скрывается сочная начинка, свежие овощи и ароматные соусы.", 30, "https://kfc-burgers.ru/wp-content/uploads/2018/11/longer-kfs.png")
# db.add_product("Чикенбургер", 25000.00, "Чикенбургер — нежная куриная котлета, свежие овощи и пикантные соусы, собранные в мягкой булочке для идеального вкуса.", 30, "https://kuponoed.ru/wp-content/uploads/2022/10/chikenburger.jpg")

users = {}
bot = TeleBot(token="7334242659:AAFhHWElOHJim9dxUGdAF86nlbd6Ke5mp9k")
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    checker = db.check_user(user_id)
    if checker == True:
        bot.send_message(user_id, "Меню: ", reply_markup=bt.main_menu_bt(user_id))
    elif checker == False:
        bot.send_message(user_id, "Выберите язык\n\n"
                                  "Tilni tanlang", reply_markup = bt.languages_in())
@bot.callback_query_handler(lambda call: call.data in ["RU","UZ"])
def calls(call):
    user_id = call.message.chat.id
    message = call.message
    if call.data =="RU":
        language = "ru"
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Добро пожаловать в бот доставки!\n\n"
                                  "Введите своё имя")
        bot.register_next_step_handler(message, get_name, language,)
    elif call.data == "UZ":
        language = "uz"
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Hush kelibsiz, etkazib berish botiga!\n\n "
                                  "Ismingizni kiriting")
        bot.register_next_step_handler(message, get_name, language)

def get_name(message,language):
    user_id = message.from_user.id
    name = message.text
    print(name)
    bot.send_message(user_id, text = tr.all_text.get("номер_т").get(language),
                     reply_markup=bt.phone_number_bt(language))
    bot.register_next_step_handler(message, get_phone, name,language)

def get_phone(message, name,language):
    user_id = message.from_user.id
    # проверяем отправил ли пользователь контакт по кнопке
    if message.contact:
        phone_number = message.contact.phone_number
        print(phone_number)
        bot.send_message(user_id, text= tr.all_text.get("локация").get(language),
                         reply_markup=bt.location_bt(language))
        bot.register_next_step_handler(message, get_location, name, phone_number,language)
    # если отправил контакт не по кнопке возвращаем в эту же функцию
    else:
        bot.send_message(user_id, text= tr.all_text.get("ошибка").get(language),
                         reply_markup=bt.phone_number_bt(language))
        bot.register_next_step_handler(message, get_phone, name,language)

def get_location(message, name, phone_number,language):
    user_id = message.from_user.id
    location = message.location
    address = geolocator.reverse((location.latitude, location.longitude)).address
    print(name, phone_number, address)
    db.add_user(name, phone_number, user_id, language)
    bot.send_message(user_id, text= tr.all_text.get("успеш_рег").get(language), reply_markup=bt.main_menu_bt(user_id))

@bot.callback_query_handler(lambda call: call.data in ["back", "cart", "plus", "minus",
                                                       "to_cart", "back_product", "order", "clear_cart"])
def calls(call):
    user_id = call.message.chat.id
    if call.data == "back":
        language = db.find_language_db(user_id)[0]
        bot.send_message(user_id, text=tr.all_text.get("меню").get(language), reply_markup=bt.main_menu_bt(user_id))
    elif call.data == "plus":
        current_amount = users.get(user_id).get("pr_count")
        users[user_id]["pr_count"] += 1
        bot.edit_message_reply_markup(user_id, call.message.id, reply_markup= bt.plus_or_minus_in(user_id,plus_or_minus="plus",
                                                                                                  current_amount = current_amount))
    elif call.data == "minus":
        current_amount = users.get(user_id).get("pr_count")
        if current_amount > 1:
            users[user_id]["pr_count"] -= 1
            bot.edit_message_reply_markup(user_id, call.message.id, reply_markup=bt.plus_or_minus_in(user_id,plus_or_minus="minus",current_amount = current_amount) )
    elif call.data == "to_cart":
        db.add_to_cart(user_id, users[user_id]["pr_id"], users[user_id]["pr_name"],
                       users[user_id]["pr_price"],users[user_id]["pr_count"])
        users.pop(user_id)
        bot.delete_message(user_id, call.message.message_id)
        all_products = db.get_pr_id_name()
        language = db.find_language_db(user_id)[0]
        bot.send_message(user_id, text=tr.all_text.get("прод_усп").get(language), reply_markup=bt.product_in(all_products,user_id))
    elif call.data=="back_product":
        bot.delete_message(user_id, call.message.message_id)
        all_products = db.get_pr_id_name()
        language = db.find_language_db(user_id)[0]
        bot.send_message(user_id, text=tr.all_text.get("выберите_п").get(language), reply_markup=bt.product_in(all_products,user_id))
    elif call.data == "cart":
        cart = db.get_user_cart(user_id)
        print(cart)
        language = db.find_language_db(user_id)[0]
        full_text =tr.all_text.get("моя_к").get(language)
        count =0
        total_price = 0
        for product in cart:
            count +=1
            full_text += f"{count}.{product[0]} x {product[1]} = {product[2]}\n"
            total_price += product[2]
        full_text += f"{tr.all_text.get("сумма").get(language)} {total_price} sum"
        cart_info = db.get_cart_id_name(user_id)
        bot.send_message(user_id, full_text, reply_markup = bt.cart_in(cart_info,user_id))
    elif call.data == "clear_cart":
        bot.delete_message(user_id, call.message.message_id)
        all_products = db.get_pr_id_name()
        language = db.find_language_db(user_id)[0]
        bot.send_message(user_id, text=tr.all_text.get("кор_уже_очищ").get(language), reply_markup=bt.product_in(all_products,user_id))
    elif call.data == "order":
        cart = db.get_user_cart(user_id)
        print(cart)
        language = db.find_language_db(user_id)[0]
        full_text = f"{"Новый заказ от пользователя "}{user_id}:\n"
        count = 0
        total_price = 0
        for product in cart:
            count += 1
            full_text += f"{count}.{product[0]} x {product[1]} = {product[2]}\n"
            total_price += product[2]
        full_text += f"{"Сумма:"} {total_price} sum"
        bot.delete_message(user_id, call.message.message_id)
        db.delete_user_cart(user_id)
        bot.send_message(admins_group, full_text)
        bot.send_message(user_id, text= tr.all_text.get("заказ_принят").get(language), reply_markup = bt.main_menu_bt(user_id))

@bot.callback_query_handler(lambda call: "prod_" in call.data)
def get_prod_info(call):
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)
    product_id = int(call.data.replace("prod_", ""))
    product_info = db.get_exact_product(product_id)
    #сохраняем кол во в хранилще
    language = db.find_language_db(user_id)[0]
    users[user_id] = {"pr_id": product_id, "pr_name": product_info[0],
                      "pr_count": 1, "pr_price": product_info[1]}
    bot.send_photo(chat_id=user_id, photo=product_info[3], caption=f"{product_info[0]}\n"
                                                                   f"{tr.all_text.get("цена").get(language)} {product_info[1]} sum\n"
                                                                   f"{tr.all_text.get("описание").get(language)} {product_info[2]}",
                   reply_markup=bt.plus_or_minus_in(user_id))

@bot.callback_query_handler(lambda call: "delete_" in call.data)
def delete_prod_cart(call):
    user_id = call.message.chat.id
    product_id = int(call.data.replace('delete_',''))
    db.delete_exact_product_from_cart(user_id, product_id)
    cart = db.get_user_cart(user_id)
    print(cart)
    language = db.find_language_db(user_id)[0]
    full_text = tr.all_text.get("моя_к").get(language)
    count = 0
    total_price = 0
    for product in cart:
        count += 1
        full_text += f"{count}.{product[0]} x {product[1]} = {product[2]}\n"
        total_price += product[2]
    full_text += f"{tr.all_text.get("сумма").get(language)} {total_price} sum"
    cart_info = db.get_cart_id_name(user_id)
    bot.edit_message_text(chat_id= user_id, message_id = call.message.message_id,
                          text= full_text, reply_markup = bt.cart_in(cart_info,user_id))

@bot.message_handler(content_types=["text"])
def text_handler(message):
    print('сработа функция отлова сообщений с контентом "текст"')
    user_id = message.from_user.id
    language = db.find_language_db(user_id)[0]
    if message.text == "🍴Меню🍴" or message.text == "🍴Menu🍴":
        all_products = db.get_pr_id_name()
        bot.send_message(user_id, text=tr.all_text.get("выберите_п").get(language), reply_markup=bt.product_in(all_products,user_id))
    elif message.text == "✍️Отзыв✍️" or message.text == "✍️Fikr-mulohaza✍️":
        bot.send_message(user_id, text= tr.all_text.get("отзыв_напишите").get(language))
        bot.register_next_step_handler(message, get_otziv)
    elif message.text == "🛒Корзина🛒" or message.text == "🛒Savatcha🛒":
        bot.send_message(message, text =tr.all_text.get("моя_к").get(language))

def get_otziv(message):
    user_id = message.from_user.id
    otziv = message.text
    print(otziv)
    full_text= (f"Отзыв от пользователя {user_id}\n"
                f"Отзыв: {otziv}")
    language = db.find_language_db(user_id)[0]
    bot.send_message(user_id, text = tr.all_text.get("отзыв_зарег").get(language),reply_markup= main_menu_bt(user_id))
    bot.send_message(admins_group,full_text)

# поддержание запуска бота
bot.infinity_polling()