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

def wait_list_cls(user):
    waitUser = models.waitlist.query.filter_by(Id = user).first()
    print (waitUser)
    if not waitUser:
        db.session.delete(waitUser)
        db.session.commit()

def menu_builder(call, user = None):
    BckStartBtn = True
    buttons = []
    text = None
    try:
        call = int(call)
    except:
        pass
    menuDate = models.menu.query.filter_by(Id = call).first()
    textDate = models.messages.query.filter_by(Id = menuDate.IdMessage).first()
         
    if menuDate.SpecAction == 'hi message newbie':
        BckStartBtn = False
        curMsg = models.messages.query.filter_by(Id = startMessage).first()
        curMsg = curMsg.Text
        text = str(textDate.Text)
        text = text % curMsg
        if not user:
            waitUser = models.waitlist.query.filter_by(Id = user).first()
            if waitUser:
                db.session.delete(waitUser)
        callSave = str(call)
        callSave = callSave[:-1]
        newUser = models.waitlist(Id = user, WhatWait = 'text', From = 'hi message newbie', 
        Call = callSave)
        db.session.add(newUser)
        db.session.commit()
            
    else:
        nextPoint = (menuDate.Id * 10) + 1
        for i in range(nextPoint,nextPoint+9):
          buttonMenuDate = models.menu.query.filter_by(Id = i).first()
          if buttonMenuDate:
              buttonDate = models.messages.query.filter_by(Id = buttonMenuDate.IdMessage).first()
              buttonText = buttonDate.ButtonText
              buttonLink = i
              buttons.append([buttonText, buttonLink])
    strCall = str(call)
    if len(strCall) != 1:
        prevMenu = '0' + strCall[:-1]
        buttons.append([backText, prevMenu]) 

    if strCall != "1" and strCall[:1] == "1" and BckStartBtn:
        buttonMenuDate = models.menu.query.filter_by(Id = 1).first()
        buttonDate = models.messages.query.filter_by(Id = buttonMenuDate.IdMessage).first()
        buttonText = buttonDate.ButtonText
        buttonLink = 1
        buttons.append([buttonText, buttonLink])
    elif strCall != "9" and strCall[:1] == "9" and BckStartBtn:
        buttonMenuDate = models.menu.query.filter_by(Id = 9).first()
        buttonDate = models.messages.query.filter_by(Id = buttonMenuDate.IdMessage).first()
        buttonText = buttonDate.ButtonText
        buttonLink = 9
        buttons.append([buttonText, buttonLink])

    return textDate, buttons, text

def need_text (text, user):
    waitUsr = models.waitlist.query.filter_by(Id = user).first()
    if waitUsr.WhatWait != 'text' and waitUsr.Id == user:
        return 'Вы должны прислать ' + waitUsr.WhatWait
    if waitUsr.From == 'hi message newbie' and waitUsr.Id == user:
        message = models.messages.query.filter_by(Id = startMessage).first()
        message.Text = text
        db.session.add(message)
        db.session.commit()
        wait_list_cls(user)
        return 'Готово',[['Назад',waitUsr.Call]]