from app import db
from app import models
from set import *
from time import sleep
from tele_bot_tools import checkMailing

def checkTask():
    '''
    Проверяет есть ли задания, которые нужно выполнить
    '''
    checkMailing()
    sleep(1)



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