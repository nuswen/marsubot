from tele_bot_tools import *
from app import models
from app import bot
from app import db


@bot.message_handler(commands=['start'])
def hi_msg(msg):
    """
    Стартовое сообщение дополнительно кодируется xxx*, где xxx команда, а * любая доп
    информация
    """

    try:
        command = msg.text[7:10] # ищем комманду в стартовом сообщении
    except:
        command = '000' # если сообщение не кодировано, скидываем в вариант по умолчанию

    if command == 'dwn': # команда на скачивание продукта
        productId = msg.text[10:]
        productData = models.Product.query.filter_by(Id = 1).first()
        productFileId = productData.FileId()
    else:
        productFileId = 0

    poster(bot, msg.chat.id, productId)

@bot.message_handler(content_types=['photo'])
def photo(msg):
    poster(bot, msg.chat.id, msg)

@bot.message_handler(content_types=['document'])
def doc(msg):
    poster(bot, msg.chat.id, msg)


@bot.message_handler(content_types=['text'])
def any_messages(msg):
    poster(bot, msg.chat.id, 'message!')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    pass