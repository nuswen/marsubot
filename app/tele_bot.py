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
            msgGo, msgDate = msg_dwn_usr(productId)
            productData = models.product.query.filter_by(Id = productId).first()
            productFileId = productData.FileIdTelega
            poster(bot, msg.chat.id, msg_start(new_tele_user(msg.chat.id)))
            poster(bot, msg.chat.id, msgGo, addTag=msgDate.TagAdd, remTag=msgDate.TagRem, 
            doc=productFileId, img=msgDate.Img)
        except:
            command = '000'
    else:
        command = '000'

    if command == '000':
            poster(bot, msg.chat.id, msg_start(new_tele_user(msg.chat.id)))

@bot.message_handler(commands=['menu'])
def menu(msg):
    textDate, buttons, text = menu_builder("1")
    if not text:
        text = textDate.Text
    poster(bot, msg.chat.id, text, addTag=textDate.TagAdd, 
    remTag=textDate.TagRem, buttons=buttons, doc=textDate.Attach, img=textDate.Img)

@bot.message_handler(commands=['smenu'])
def smenu(msg):
    textDate, buttons, text = menu_builder("9")
    if not text:
        text = textDate.Text
    poster(bot, msg.chat.id, text, addTag=textDate.TagAdd, 
    remTag=textDate.TagRem, buttons=buttons, doc=textDate.Attach, img=textDate.Img)

@bot.message_handler(content_types=['photo'])
def photo(msg):
    poster(bot, msg.chat.id, msg)

@bot.message_handler(content_types=['document'])
def doc(msg):
    poster(bot, msg.chat.id, msg)


@bot.message_handler(content_types=['text'])
def any_messages(msg):
    # TODO добавить возможность менять тэги
    text, buttons = need_text(msg.text, msg.chat.id)
    poster(bot, msg.chat.id, text, buttons=buttons)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data[0] == '0':
        wait_list_cls(call.message.chat.id)
        call.data = call.data[1:]
    
    textDate, buttons, text = menu_builder(call.data, call.message.chat.id)

    if not text:
        text = textDate.Text

    poster(bot, call.message.chat.id, text, addTag=textDate.TagAdd, 
    remTag=textDate.TagRem, buttons=buttons, doc=textDate.Attach, img = textDate.Img,
    ed = True, message_id=call.message.message_id)