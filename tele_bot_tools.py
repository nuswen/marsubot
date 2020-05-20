from telebot import types
from app import models
from app import db
import json
import re
from app import bot
from tools import *
from set import *
from datetime import datetime,date,time

def poster(bot, chatId, text=None, buttons=None, ed=False, message_id=None, doc=None, img=None,inline=False,lenRow=None):
    if buttons:
        if ed and not img and not doc:
            bot.edit_message_text(chat_id=chatId, message_id=message_id, text=text, reply_markup=keyboarder(buttons,inline,lenRow))
        else:
            if img:
                bot.send_photo(chat_id=chatId, photo=img, reply_markup=keyboarder(buttons,inline,lenRow))
            if text:
                bot.send_message(chatId, text, reply_markup=keyboarder(buttons,inline,lenRow))
            if doc:
                bot.send_document(chat_id=chatId, data=doc, reply_markup=keyboarder(buttons,inline,lenRow))
    else:
        if ed and not img and not doc:
            bot.edit_message_text(chat_id=chatId, message_id=message_id, text=text)
        else:
            if img:
                bot.send_photo(chat_id=chatId, photo=img)
            if text:
                bot.send_message(chatId, text)
            if doc:
                bot.send_document(chat_id=chatId, data=doc)

def keyboarder(keys,inline,lenRow):
    if inline: 
        return inlineKeyboarder(keys,lenRow=lenRow)
    else: 
        return clasicKeyboarder(keys)

def isUrl(text):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', re.IGNORECASE)
    print(re.match(regex, text) is not None)
    return re.match(regex, text) is not None

def inlineKeyboarder(rows, lenRow=None):
    if not lenRow: lenRow=10
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = lenRow
    keysRows = []
    rowCount = 0

    for row in rows:
        keysRows.append([])
        rowCount = len(keysRows)-1
        for key in row:
            keyValue = json.dumps(row[key])
            keyValue = keyValue.strip('"')
            if isUrl(keyValue):
                keysRows[rowCount].append(types.InlineKeyboardButton(text=key, url=keyValue))
            else:
                keysRows[rowCount].append(types.InlineKeyboardButton(text=key, callback_data=keyValue))
    
    for row in keysRows:
        if len(row) == 1:
            keyboard.add(row[0])
        elif len(row) == 2:
            keyboard.add(row[0],row[1])
        elif len(row) == 3:
            keyboard.add(row[0],row[1],row[2])
        elif len(row) == 4:
            keyboard.add(row[0],row[1],row[2],row[3])
        elif len(row) == 5:
            keyboard.add(row[0],row[1],row[2],row[3],row[4])
        elif len(row) == 6:
            keyboard.add(row[0],row[1],row[2],row[3],row[4],row[5])
        elif len(row) == 7:
            keyboard.add(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
        elif len(row) == 8:
            keyboard.add(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
        elif len(row) == 9:
            keyboard.add(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
        elif len(row) == 10:
            keyboard.add(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])
            
    return keyboard

def clasicKeyboarder(keys):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    temp = []
    for i in keys:
        temp.append(i)
    temp.reverse()
    for i in temp:
        keyboard.add(i)
    return keyboard

def new_tele_user(usrId):
    '''
    Пытается добавить нового юзера в базу - возвращает start если вышло, если юзверь 
    уже есть - continue
    '''
    #TODO Добавлять часовой пояс
    exUser = models.teleusers.query.filter_by(Id = usrId).first()
    if exUser:
        return 'continue'
    newUser = models.teleusers(Id = usrId,
                                Tags = [],
                                Tunels = {},
                                LastAct = int(datetime.now().timestamp()),
                                isAdmin = False,
                                isOperator = False)
    db.session.add(newUser)
    db.session.commit()
    return 'start'

def openTeleMailing(userId):
    '''
    Открывает возможность составления рассылки для пользователя
    '''
    user = models.teleusers.query.filter_by(Id = userId).first()
    if 'mailingOpen' in user.Tags:
        return
    newMailing = models.mailinglist(Messages = {},
                                    userCreator = userId,
                                    isClosed = False,
                                    Done = False)
    user.Tags.append('mailingOpen')
    models.teleusers.query.filter_by(Id = userId).update({'Tags':user.Tags})
    db.session.add(newMailing)
    db.session.commit()
    msgDate = models.messages.query.filter_by(Id = openTeleMailingMessage).first()
    poster(bot, userId, msgDate.Text)

def isAdmin(userId):
    '''
    Принимает Id телеграмм пользователя - возвращает boolean является ли он админом
    '''
    user = models.teleusers.query.filter_by(Id = userId).first()
    return user.isAdmin

def teleIn(msg):

    print(msg)
    '''
    Разбирает куда отправить сообщение от пользователя
    '''
    # Смотрим что за пользователь
    user = models.teleusers.query.filter_by(Id = msg.chat.id).first()
    if not user:
        poster(bot, msg.chat.id, msg_start(new_tele_user(msg.chat.id)))
    # Проходимся по тегам
    for tag in user.Tags:
        if tag == 'mailingOpen': #  Если у юзера открыта сессия составления рассылки
            toMailingMsgs(msg)
            return
    # Если некуда деть сообщение считаем, что оно предназначено оператору
    if user.isOperator is False:
        operators = models.teleusers.query.filter_by(isOperator = True).all()
        for operator in operators:
            bot.forward_message(operator.Id, user.Id, msg.message_id)
    elif user.isOperator is True:
        if  True:
            poster(bot,msg.json.reply_to_message.forward_from.id,msg.text)

def toMailingMsgs(msg):
    '''
    Добавляет в рассылку сообщение
    '''
    mailing = models.mailinglist.query.filter_by(userCreator = msg.chat.id, isClosed = False).first()
    # Ищем номер след сообщения numMsg
    if mailing.Messages == {}:
        numMsg = 0
    else:
        numMsg = []
        for i in mailing.Messages:
            numMsg.append(int(i))
        numMsg.sort()
        numMsg = numMsg[-1] + 1
    print(msg)
    # В зависимости от типа сообщения создаём новое
    if msg.content_type == 'text':
        newMsg = {numMsg:{'text':msg.text,'img':None,'attach':None}}
    elif msg.content_type == 'photo':
        newMsg = {numMsg:{'text':msg.caption,'img':msg.photo[-1].file_id,'attach':None}}
    elif msg.content_type == 'document':
        newMsg = {numMsg:{'text':msg.caption,'img':None,'attach':msg.document.file_id}}

    mailing.Messages.update(newMsg)
    models.mailinglist.query.filter_by(userCreator = msg.chat.id, isClosed = False).update({'Messages':mailing.Messages})
    db.session.commit()

    print(newMsg)

def closeMailing(userId,closeDataTime):
    '''
    Закрывает сессию добавления постов к рассылке, указывает время отправки рассылки
    '''
    #TODO Учитывать часовой пояс
    # Делаем из входящего формата строки "час минуты день месяц" timestamp
    closeDataTime = closeDataTime.split()
    today = date.today()
    curYear = today.timetuple()[0]
    try:
        t = time(int(closeDataTime[0]),int(closeDataTime[1]))
        d = date(curYear,int(closeDataTime[3]),int(closeDataTime[2]))
        if today > d:
            d = date(curYear+1,int(closeDataTime[3]),int(closeDataTime[2]))
        dt = datetime.combine(d, t)
        models.mailinglist.query.filter_by(userCreator = userId, isClosed = False).update({'UnixTimeToGo':int(dt.timestamp()),
                                                                                            'isClosed':True})
        user = models.teleusers.query.filter_by(Id = userId).first()
        try:
            user.Tags.remove('mailingOpen')
            models.teleusers.query.filter_by(Id = userId).update({'Tags':user.Tags})
        except Exception as e:
            pass
        db.session.commit()
        print(int(datetime.now().timestamp()))
        print(int(dt.timestamp()))
    except Exception as e:
        print(e)