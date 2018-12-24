from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

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
        body = request.body.decode()
        logging.info("Request body: " + body)

        logging.debug(f'signature: {signature}')

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            # abort(400)
            return HttpResponseForbidden('invalid signature')

        return 'OK'
    return HttpResponseForbidden()


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    logging.debug('handle_message')
    logging.debug(f'reply_token: {event.reply_token}')
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
