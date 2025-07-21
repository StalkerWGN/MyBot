import telebot
from telebot import types
from flask import Flask, request
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Создаем Flask-приложение
app = Flask(__name__)

TOKEN = os.getenv('TELEGRAM_API_TOKEN')  # Используем переменную окружения для токена
bot = telebot.TeleBot(TOKEN)

# Обработка вебхуков
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

# Настройка webhook
@app.route('/setwebhook', methods=['GET'])
def set_webhook():
    webhook_url = os.getenv('WEBHOOK_URL')  # Адрес для вашего webhook (платформа Render)
    
    # Сначала удаляем старый webhook
    bot.remove_webhook()

    # Устанавливаем новый webhook
    bot.set_webhook(url=webhook_url)

    # Логируем статус вебхука
    webhook_info = bot.get_webhook_info()
    logger.info(f"Webhook info: {webhook_info}")

    return f'Webhook set to {webhook_url}', 200

# Обработчики сообщений и команд
@bot.message_handler(commands=['start'])
def start(message):
    logger.debug(f"Processing /start command from {message.chat.id}")
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
    btn = types.InlineKeyboardButton("Подписка", callback_data="subscribe")
    markup.add(btn)

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='HTML', disable_web_page_preview=True)

@bot.callback_query_handler(func=lambda call: call.data == "subscribe")
def handle_subscription(call):
    logger.debug(f"User {call.message.chat.id} selected 'subscribe'")
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("SPF☀️ОТПУСК", callback_data="spf_option")
    markup.add(btn)
    bot.send_message(call.message.chat.id, "Подписки:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "spf_option")
def handle_spf(call):
    logger.debug(f"User {call.message.chat.id} selected 'spf_option'")
    try:
        photo = open('spf.jpg', 'rb')  # Убедитесь, что файл существует
    except FileNotFoundError:
        photo = None  # В случае отсутствия файла, просто пропустим

    caption = (
        "<b>SPF☀️ОТПУСК</b>\n"
        "⭐️Теперь никакого маркетинга.\n"
        "⭐️Выбор средства только исходя из ваших новых знаний."
    )

    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("Условия подписки", callback_data="terms")
    markup.add(btn)

    bot.send_photo(call.message.chat.id, photo, caption=caption, reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == "terms")
def handle_terms(call):
    logger.debug(f"User {call.message.chat.id} selected 'terms'")
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
    pay_btn = types.InlineKeyboardButton("Оплатить 990р/месяц", url="https://yookassa.ru/")
    markup.add(pay_btn)

    bot.send_message(
        call.message.chat.id,
        text,
        reply_markup=markup,
        parse_mode='HTML',
        disable_web_page_preview=True
    )

# Запуск Flask-приложения
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
