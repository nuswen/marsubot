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

@bot.message_handler(commands=['menu'])
def menu(msg):
    textDate, buttons = menu_builder('1')
    
    if textDate[:-1] != []:
        for i in textDate[:-1]:
          poster(bot, msg.message.chat.id, i.Text, addTag=i.TagAdd, 
          remTag=i.TagRem, doc=i.Attach, img = i.Img)

        i = textDate[-1]
        poster(bot, msg.message.chat.id, i.Text, addTag=i.TagAdd, 
          remTag=i.TagRem, buttons=buttons, doc=i.Attach, img = i.Img)
    else:
        i = textDate[0]
        print (str(msg))
        poster(bot, msg.chat.id, i.Text, addTag=i.TagAdd, 
          remTag=i.TagRem, buttons=buttons, doc=i.Attach,
              img = i.Img)

@bot.message_handler(commands=['smenu'])
def smenu(msg):
    textDate, buttons = menu_builder('9')
    
    if textDate[:-1] != []:
        for i in textDate[:-1]:
            poster(bot, msg.chat.id, i.Text, addTag=i.TagAdd, 
            remTag=i.TagRem, doc=i.Attach, img = i.Img)

        i = textDate[-1]
        poster(bot, msg.chat.id, i.Text, addTag=i.TagAdd, 
        remTag=i.TagRem, buttons=buttons, doc=i.Attach, img = i.Img)
    else:
        i = textDate[0]
        poster(bot, msg.chat.id, i.Text, addTag=i.TagAdd, 
        remTag=i.TagRem, buttons=buttons, doc=i.Attach,
        img = i.Img)

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
    
    textDate, buttons = menu_builder(call.data, call.message.chat.id)
    
    if len(textDate) > 1:
        for i in textDate[:-1]:
            print (textDate)
            print (i)
            print (i.Text)
            poster(bot, call.message.chat.id, i.Text, addTag=i.TagAdd, 
            remTag=i.TagRem, doc=i.Attach, img = i.Img)

        i = textDate[-1]
        poster(bot, call.message.chat.id, i.Text, addTag=i.TagAdd, 
        remTag=i.TagRem, buttons=buttons, doc=i.Attach, img = i.Img)
    else:
        i=textDate[0]
        poster(bot, call.message.chat.id, i.Text, addTag=i.TagAdd, 
        remTag=i.TagRem, buttons=buttons, doc=i.Attach,
        img = i.Img, ed = True, message_id=call.message.message_id)