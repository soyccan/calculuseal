from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage
)

import threading
import logging
logging.getLogger().setLevel('DEBUG')

import calculuseal.settings

# app = Flask(__name__)

line_bot_api = LineBotApi('ncgm9HizxV7Z1qyLCQtYTlLfH77C497/1LflP9CroAgEavL6BxyQK6JFY2Joa02EnXx8MUtGjrpGN8ueV2dEbSrsi/nyHgE5aQVw79jnKI8yqQtHvkvBKGYnOWCb6bosC4qhWmfdnANYspooKzmsnQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('90710d30a6a5618caea6ef52bc0fed7e')


# @app.route("/callback", methods=['POST'])
# def callback():
def webhook(request):
    if calculuseal.settings.DEBUG == True or request.method == 'POST':
        # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']

        # get request body as text
        body = request.body.decode('utf-8', 'ignore') # TODO: handle UnicodeError
        logging.info("Request body: " + body)

        logging.debug(f'signature: {signature}')

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            # abort(400)
            return HttpResponseForbidden('invalid signature')

        # reply 200 OK within one second (otherwise LINE will see it as bad request)
        return HttpResponse()

    return HttpResponseForbidden()


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    logging.debug('handle_text_message')
    logging.debug(f'reply_token: {event.reply_token}')
    t = threading.Thread(target=reply_to_line, args=(event.reply_token, event.message.text))
    t.join()

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    logging.debug('handle_image_message')
    logging.debug(f'reply_token: {event.reply_token}')

    # receive image
    imgdata = requests.get(f'https://api.line.me/v2/bot/message/{event.message.id}/content').content
    logging.debug(f'writting to /tmp/_in.jpg')
    open(calculuseal.settings.BASE_DIR + '/tmp/_in.jpg', 'wb').write(imgdata)

    # reply image
    # TODO

    # threading.Thread(target=reply_to_line, args=(event.reply_token, event.message.???))

def reply_to_line(reply_token, text):
    logging.debug(f'reply_message: token={reply_token} text={text}')
    line_bot_api.reply_message(
        reply_token,
        TextSendMessage(text=text))
