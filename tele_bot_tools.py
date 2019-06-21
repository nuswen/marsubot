from telebot import types


def poster(bot, chat_id, text, buttons=None, ed=False, message_id=None, doc=None):
    if buttons:
        if ed:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=keyboarder(buttons))
        else:
            bot.send_message(chat_id, text, reply_markup=keyboarder(buttons))
    else:
        if ed:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
        else:
            bot.send_message(chat_id, text)
            if doc:
                bot.send_document(chat_id=chat_id, data=doc)


def keyboarder(keys):
    keyboard = types.InlineKeyboardMarkup()
    for key in keys:
        keyboard.add(types.InlineKeyboardButton(text=key[1], callback_data=key[2]))
    return keyboard


def get_phone_number(bot, chat_id, text):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(chat_id, text, reply_markup=keyboard)
