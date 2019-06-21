from telebot import types
from app import models
from app import db


def poster(bot, chatId, text, addTag=None, remTag=None, buttons=None, ed=False, message_id=None, doc=None):
    if addTag or remTag:
        usr = models.teleusers.query.filter_by(Id = chatId).first()
        tags = usr.Tags
        if addTag:
            for i in addTag:
                if i not in tags:
                    tags.append(i)
        elif remTag:
            for i in tags:
                if i in remTag:
                    tags.remove(i)
        usr.Tags = tags
        db.session.add(usr)
        db.session.commit()
    
    if buttons:
        if ed:
            bot.edit_message_text(chat_id=chatId, message_id=message_id, text=text, reply_markup=keyboarder(buttons))
        else:
            bot.send_message(chatId, text, reply_markup=keyboarder(buttons))
            if doc:
                bot.send_document(chat_id=chatId, data=doc)
    else:
        if ed:
            bot.edit_message_text(chat_id=chatId, message_id=message_id, text=text)
        else:
            bot.send_message(chatId, text)
            if doc:
                bot.send_document(chat_id=chatId, data=doc)


def keyboarder(keys):
    keyboard = types.InlineKeyboardMarkup()
    for key in keys:
        keyboard.add(types.InlineKeyboardButton(text=key[1], callback_data=key[2]))
    return keyboard


def new_user(usrId):
    exUser = models.teleusers.query.filter_by(Id = usrId).first()
    if exUser:
        return 'exUser'
    newUser = models.teleusers(Id = usrId)
    db.session.add(newUser)
    db.session.commit()
