from os import environ
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import telebot
import threading
import json
import requests

bot = telebot.TeleBot(environ['token'])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']
db = SQLAlchemy(app)


from app import tele_bot, models

@app.before_first_request
def activate_job():
    def checkTask_worker():
        from tools import checkTask
        while True:
            checkTask()

    thread = threading.Thread(target=checkTask_worker)
    thread.start()

@app.route('/facebookbot/test/', methods=['GET'])
def test():
    btns = {
            "type":"postback",
            "title":"<BUTTON_TEXT>",
            "payload":"<DEVELOPER_DEFINED_PAYLOAD>"
            }
    send_text_message('2241087689304329', 'message_text',buttons=btns)
    return "200"

@app.route('/facebookbot/privacy/', methods=['GET'])
def privacy():
    privacy_file = open('privacy.txt')
    return privacy_file.read()

@app.route('/facebookwebhook/', methods=['GET'])
def verify():
    print(request)
    if (request.args.get('hub.verify_token', '') == environ['facebook_verify_token']):
        print("Verified")
        return request.args.get('hub.challenge', '')
    else:
        print('wrong verification token')
        return "Error, Verification Failed"

@app.route('/facebookwebhook/', methods=['POST'])
def handle_messages():
    data = request.get_json()
    entry = data['entry'][0]
    print(data)

    if entry.get("messaging"):
        messaging_event = entry['messaging'][0]
        sender_id = messaging_event['sender']['id']
        if messaging_event.get("message"):
            message_text = messaging_event['message']['text']
            send_text_message(sender_id, message_text)
        else:
            print(messaging_event)
    return 'ok', 200

def send_text_message(recipient_id, message, buttons=None):
    data = json.dumps({
        "recipient": {"id": recipient_id},
        "message": {"text": message,"buttons":buttons}})
 
    params = {
        "access_token": environ['facebook_token']
    }
 
    headers = {
        "Content-Type": "application/json"
    }
 
    r = requests.post(
        "https://graph.facebook.com/v7.0/me/messages",
        params=params, headers=headers, data=data
    )

@app.route("/"+environ['token'], methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


bot.remove_webhook()
bot.set_webhook(url=environ['app_url']+environ['token'])
print(environ.get('PORT', 5000))
app.run(host="0.0.0.0", port=int(environ.get('PORT', 5000)))