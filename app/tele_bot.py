from tele_bot_tools import *
from tools import *
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
        try:
            productId = int(msg.text[10:])
            msgGo, msgDate, productData = msg_dwn_usr(productId)
            productFileId = productData.FileIdTelega
            poster(bot, msg.chat.id, msg_start(new_tele_user(msg.chat.id)))
            print(msgDate.Img)
            poster(bot, msg.chat.id, msgGo, doc=productFileId, img=productData.Img)
        except:
            command = '000'
    else:
        command = '000'

    if command == '000':
            poster(bot, msg.chat.id, msg_start(new_tele_user(msg.chat.id)))

@bot.message_handler(commands=['mailing'])
def mailing(msg):
    if isAdmin(msg.chat.id):
        openTeleMailing(msg.chat.id)


@bot.message_handler(content_types=['text'])
def any_messages(msg):
    teleIn(msg)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    pass