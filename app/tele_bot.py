from tele_bot_tools import *
from app import models
from app import bot
from app import db


@bot.message_handler(commands=['start'])
def hi_msg(msg):
    poster(bot, msg.chat.id, msg)

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