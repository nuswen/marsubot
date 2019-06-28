from app import db
from app import models
from set import *

def msg_dwn_usr(productId):
    """
    Принимает Id продукта и отдает составленное сообщение для отправки
    """
    productData = models.product.query.filter_by(Id = productId).first()
    msgId = productData.MessageId
    msgDate = models.messages.query.filter_by(Id = msgId).first()
    name = productData.ProductName
    text = msgDate.Text % name
    return text, msgDate

def msg_start(first):
    if first == 'start':
        msgDate = models.messages.query.filter_by(Id = startMessage).first()
    elif first == 'continue':
        msgDate = models.messages.query.filter_by(Id = msgContinue).first()
    text = msgDate.Text
    return text

def menu_builder(call):
    menuDate = models.menu.query.filter_by(Id = call).first()
    textDate = models.messages.query.filter_by(Id = menuDate.IdMessage).first()
    nextPoint = (menuDate.Id * 10) + 1
    buttons = []
    for i in range(nextPoint,nextPoint+9):
        buttonMenuDate = models.menu.query.filter_by(Id = i).first()
        if buttonMenuDate:
            buttonDate = models.messages.query.filter_by(Id = buttonMenuDate.IdMessage).first()
            buttonText = buttonDate.ButtonText
            buttonLink = i
            buttons.append([buttonText, buttonLink])
    if call != "1":
        buttonMenuDate = models.menu.query.filter_by(Id = 1).first()
        buttonDate = models.messages.query.filter_by(Id = buttonMenuDate.IdMessage).first()
        buttonText = buttonDate.ButtonText
        buttonLink = 1
        buttons.append([buttonText, buttonLink])
    elif call > "1000000000":
        buttonMenuDate = models.menu.query.filter_by(Id = 1000000000).first()
        buttonDate = models.messages.query.filter_by(Id = buttonMenuDate.IdMessage).first()
        buttonText = buttonDate.ButtonText
        buttonLink = 1000000000
        buttons.append([buttonText, buttonLink])

    return textDate, buttons