from tele_bot_tools import *
from app import models
from app import bot
from app import db


@bot.message_handler(commands=['start'])
def hi_msg(msg):
    poster(bot, msg.chat.id, 'hi!')


@bot.message_handler(content_types=['text'])
def any_messages(msg):
    num = models.num.query.filter_by(id=1).first()
    poster(bot, msg.chat.id, 'message!'+str(num))


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    pass