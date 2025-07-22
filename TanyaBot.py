import os
from flask import Flask, request
import telebot
from telebot import types

# Инициализация
TOKEN = os.getenv('TELEGRAM_API_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

if not TOKEN:
    raise ValueError("TELEGRAM_API_TOKEN не установлен в переменных окружения")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Webhook обработчик
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return 'OK', 200
    else:
        return 'Unsupported Media Type', 415

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "Здравствуйте!  \n\n"
        "👩🏻‍⚕️<b> Я — Доктор и Репетитор Татьяна Кузина. </b>👩🏻‍🎓\n\n"
        "🌿Создатель проектов:\n"
        "<a href=\"https://dr-tatiana-kuzina.ru/\">• Личного сайта</a>\n"
        "<a href=\"https://www.youtube.com/@dr_tatyana_kusina\">• YouTube-канала</a>\n"
        "<a href=\"https://rutube.ru/channel/50702550/\">• RuTube-канала</a>\n"
        "<a href=\"https://t.me/dr_tatyana_kusina\">• Telegram-канала</a>\n"
        "<a href=\"https://vk.com/dr_tatyana_kuzina\">• ВК-группы</a>\n"
        "<a href=\"https://profi.ru/profile/IlyushinaTS\">• Профи.ру-отзывы</a>\n\n"
        "Приветствую вас в своём боте!\n\n"
        "✔️Бот поможет вам получить всю необходимую информацию по подписке на частный канал и саму подписку."
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Подписка", callback_data="subscribe"))
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='HTML', disable_web_page_preview=True)

# Обработка нажатия "Подписка"
@bot.callback_query_handler(func=lambda call: call.data == "subscribe")
def handle_subscription(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("SPF☀️ОТПУСК", callback_data="spf_option"))
    bot.send_message(call.message.chat.id, "Подписки:", reply_markup=markup)

# Обработка нажатия SPF
@bot.callback_query_handler(func=lambda call: call.data == "spf_option")
def handle_spf(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Условия подписки", callback_data="terms"))

    caption = (
        "<b>SPF☀️ОТПУСК</b>\n"
        "⭐️Теперь никакого маркетинга.\n"
        "⭐️Выбор средства только исходя из ваших новых знаний."
    )

    try:
        with open('spf.jpg', 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=markup, parse_mode='HTML')
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, caption, reply_markup=markup, parse_mode='HTML')

# Обработка нажатия условий
@bot.callback_query_handler(func=lambda call: call.data == "terms")
def handle_terms(call):
    text = (
        "⏳<b>Длительность подписки</b>\n"
        "— 30 суток.\n\n"
        "💎<b>Стоимость подписки</b>\n"
        "— 990 рублей.\n\n"
        "⌛️По окончании подписки вы будете удалены из канала.\n"
        "Автоматического продления подписки нет.\n\n"
        "📄Перед оплатой ознакомьтесь с условиями <a href=\"https://docs.google.com/document/d/1Qj5l-5LFDLkDQmWOTmaZty1zdWM6jA37/edit?usp=drivesdk&ouid=115678023785167711130&rtpof=true&sd=true\">Оферты</a>.\n\n"
        "Оплачивая подписку, вы автоматически подтверждаете, что ознакомлены с условиями оферты и принимаете их.\n\n"
        "❗️<b>Напоминание по поводу нарушения авторских прав</b>:\n"
        "При краже контента частного канала человек несёт:\n"
        "— административную ответственность\n"
        "(штраф до 5 млн рублей по решению суда),\n"
        "— уголовную ответственность\n"
        "(ст.146 УК РФ).\n\n"
        "<b>⚙️Техподдержка бота</b>\n"
        "По техническим вопросам необходимо обращаться в аккаунт Поддержки бота @HakuSonThunder.\n"
        "Если нет ответа, повторно писать не нужно.\n\n"
"🏝️Частный канал\n"
        "«<b>SPF☀️ОТПУСК</b>»\n"
        "наполнен невероятно важной, необходимой информацией для каждого, кто хочет сохранить здоровье и красоту своей кожи и не только!🍀\n"
        "Вас ждёт сказочно красивый, атмосферный и, самое главное, понятный и полезный контент!🌷"
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Оплатить 990р/месяц", url="https://yookassa.ru/"))

    bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode='HTML', disable_web_page_preview=True)

# Запуск приложения
if name == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
