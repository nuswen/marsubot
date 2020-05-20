from app import db
from app import models
from set import *
from time import sleep
from datetime import datetime,date,time


def checkTask():
    '''
    Проверяет есть ли задания, которые нужно выполнить
    '''
    checkMailing()
    sleep(1)

def checkMailing():
    '''
    Чекает, не пора бы отправлять рассылку
    '''
    print('work')
    mailings = models.mailinglist.query.filter_by(Done = False, isClosed = True).all()
    tsn = int(datetime.now().timestamp())
    for mailing in mailings:
        if tsn<=mailing.UnixTimeToGo:
            sendMailing(mailing)

def sendMailing(mailing):
    '''
    Рассылает рассылку по списку
    '''
    #TODO Сделать ранжирование по тэгам
    #TODO Добавить в рассылку кнопки и пр интерактив
    #TODO Разбить на потоки

    users = models.teleusers.query.all()
    order = []
    for msgNum in mailing.Messages:
        order.append(int(msgNum))
    order.sort()

    for user in users:
        for i in order:
            poster(bot,user.Id,mailing.Messages[str(i)]['text'],
                    img=mailing.Messages[str(i)]['img'],
                    doc=mailing.Messages[str(i)]['attach'])
    models.mailinglist.query.filter_by(Id = mailing.Id).update({'Done':True})
    db.session.commit()

def msg_dwn_usr(productId):
    """
    Принимает Id продукта и отдает составленное сообщение для отправки
    """
    productData = models.product.query.filter_by(Id = productId).first()
    msgId = productData.MessageId
    msgDate = models.messages.query.filter_by(Id = msgId).first()
    name = productData.ProductName
    text = msgDate.Text % name
    return text, msgDate, productData

def msg_start(first):
    """
    Принимает строку'start'/'continue' возвращает нужное сообщение приветствия
    """
    if first == 'start':
        msgDate = models.messages.query.filter_by(Id = startMessage).first()
    elif first == 'continue':
        msgDate = models.messages.query.filter_by(Id = msgContinue).first()
    text = msgDate.Text
    return text