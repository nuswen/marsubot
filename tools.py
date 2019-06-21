from app import db
from app import models

def msg_dwn_new_usr(productId):
    """
    Принимает Id продукта и отдает составленное сообщение для отправки
    """
    productData = models.product.query.filter_by(Id = productId).first()
    msgId = productData.MessageId
    msgDate = models.messages.query.filter_by(Id = msgId).first()
    url = productData.DownloadLink
    name = productData.ProductName
    text = msgDate.Text % (name + '/n/n' + url + '/n/n')
    return text