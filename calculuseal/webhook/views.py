from urllib.parse import quote
import threading
import os
import os.path
import logging
import pprint
import time

from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage
)

import calculuseal.settings
from webhook import models
from apis import mathpix, wolfram

# app = Flask(__name__)

logging.getLogger().setLevel('DEBUG')
line_bot_api = LineBotApi('ncgm9HizxV7Z1qyLCQtYTlLfH77C497/1LflP9CroAgEavL6BxyQK6JFY2Joa02EnXx8MUtGjrpGN8ueV2dEbSrsi/nyHgE5aQVw79jnKI8yqQtHvkvBKGYnOWCb6bosC4qhWmfdnANYspooKzmsnQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('90710d30a6a5618caea6ef52bc0fed7e')


def media(request, timestamp):
    obj = models.Media.objects.filter(timestamp=timestamp)[0]
    # TODO: audio and video
    if obj.media_type == 'i':
        # image
        # TODO: other image type (png, gif...)
        return HttpResponse(bytes(obj.image), content_type='image/jpeg')
    else:
        return HttpResponseBadRequest()

# @app.route("/callback", methods=['POST'])
# def callback():
def webhook(request):
    logging.debug('request:')
    logging.debug(vars(request))

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
    t = threading.Thread(target=reply_text, args=(event.reply_token, event.message.text))
    t.start()

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    logging.debug('handle_image_message')
    logging.debug(f'reply_token: {event.reply_token}')

    # img_dir = os.path.join(calculuseal.settings.BASE_DIR, 'static', 'media')
    # in_img_path = os.path.join(img_dir, "_in.jpg")


    # receive image
    # TODO: optimize with iter_content()
    problem = line_bot_api.get_message_content(event.message.id).content
    logging.debug(f'problem: {problem[:20]}')

    # logging.debug(f'writing to {in_img_path}')

    # reply image
    # equation = mathpix.translate(in_img_path)
    equation = mathpix.translate(problem)
    answers = wolfram.solve(equation)
    if not answers:
        t = threading.Thread(target=reply_text, args=(event.reply_token, '我看不懂！'))
        t.start()
        return
    for ans in answers:
        timestamp = int(time.time())
        models.Media(timestamp=timestamp, image=ans, media_type='i').save()

        logging.debug(f'ans: {ans[:20]}, timestamp={timestamp}')
        t = threading.Thread(target=reply_image, args=(event.reply_token, timestamp))
        t.start()

def reply_text(reply_token, text):
    logging.debug(f'reply_message: token={reply_token} text={text}')
    line_bot_api.reply_message(
        reply_token,
        TextSendMessage(text=text))

def reply_image(reply_token, timestamp):
    logging.debug(f'reply_message: token={reply_token} timestamp={timestamp}')

    imgurl = 'https://' + quote(calculuseal.settings.SERVER_NAME + f'/media/{timestamp}')
    logging.debug(f'imgurl={imgurl}')

def reply_image_img_path(reply_token, img_path):
    logging.debug(f'reply_message: token={reply_token} image={img_path}')

    subpath = img_path[len(calculuseal.settings.BASE_DIR) : ]
    imgurl = 'https://' + quote(calculuseal.settings.SERVER_NAME + subpath)
    logging.debug(f'servername={calculuseal.settings.SERVER_NAME}, subpath={subpath}')
    logging.debug(f'imgurl={imgurl}')

    line_bot_api.reply_message(
        reply_token,
        ImageSendMessage(original_content_url=imgurl, preview_image_url=imgurl))
