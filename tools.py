from app import db
from app import models
from set import *

def msg_dwn_new_usr(productId):
    """
    Принимает Id продукта и отдает составленное сообщение для отправки
    """
    productData = models.product.query.filter_by(Id = productId).first()
    msgId = productData.MessageId
    msgDate = models.messages.query.filter_by(Id = msgId).first()
    name = productData.ProductName
    text = msgDate.Text % name
    return text

def msg_start():
    msgDate = models.messages.query.filter_by(Id = startMessage).first()
    text = msgDate.Text
    return text