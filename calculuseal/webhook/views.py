from urllib.parse import quote
import threading
import os
import os.path
import logging
import json
import time
import re

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
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage,
    FollowEvent
)

import calculuseal.settings
import config.line
from webhook import models
from apis import mathpix, wolfram

# app = Flask(__name__)

line_bot_api = LineBotApi(config.line.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.line.CHANNEL_SECRET)


def media(request, timestamp):
    obj = models.Media.objects.filter(timestamp=timestamp)[0]
    # TODO: audio and video
    if obj.content_type.startswith('image/'):
        return HttpResponse(bytes(obj.data), content_type=obj.content_type)
    else:
        return HttpResponseBadRequest()

# @app.route("/callback", methods=['POST'])
# def callback():
def webhook(request):
    logging.debug('request:')
    logging.debug(vars(request))

    if request.method == 'POST':
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
    logging.debug(f'handle_text_message user={event.source.user_id}')
    logging.debug(f'reply_token: {event.reply_token}')

    words = event.message.text
    calc_suc = False # if calculation succeded

    if re.match(r'[0-9+\-*/^().<>=]*', words):
        try:
            result = eval(words)
            calc_suc = True
        except:
            calc_suc = False

    if calc_suc:
        reply_message(event.reply_token, ['當恁爸計算機哦', words + ' = ' + str(result)])
    else:
        reply_message(event.reply_token, ['我聽不懂所以只能重複你說的話', words])

    # t = threading.Thread(target=reply_text, args=(event.reply_token, event.message.text))
    # t.start()

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    logging.debug(f'handle_image_message user={event.source.user_id}')
    logging.debug(f'reply_token: {event.reply_token}')

    # receive image
    # TODO: optimize with iter_content()
    problem = line_bot_api.get_message_content(event.message.id).content
    logging.debug(f'problem: {problem[:20]}')

    # push image
    equation = mathpix.translate(problem)
    answers = wolfram.solve(equation)
    if not answers:
        push_message(event.source.user_id, ['我不會！！！'])
        # t = threading.Thread(target=push_text, args=(event.source.user_id, '我不會！！！'))
        # t.start()
        return
    timestamps = []
    for ans, content_type in answers:
        timestamp = int(time.time() * 1000)
        models.Media(timestamp=timestamp, data=ans, preview_data=ans, content_type=content_type).save()
        logging.debug(f'ans: {ans[:20]}, timestamp={timestamp}')
        timestamps.append(timestamp)

    push_image(event.source.user_id, timestamps)
    # t = threading.Thread(target=push_image, args=(event.source.user_id, timestamps))
    # t.start()

@handler.add(FollowEvent)
def handle_follow(event):
    # TODO: email the developer
    logging.debug(f'{event.source.user_id} followed me ^_^')
    profile = json.loads(line_bot_api.get_profile(event.source.user_id, timeout=10).__str__())
    logging.debug(f'his/her profile:')
    logging.debug(profile)
    push_message(config.line.DEVELOPER_ID, ['some friendly fellow followed me ^_^', profile.__str__()])

def reply_message(reply_token, messages):
    logging.debug(f'reply_message: token={reply_token} text={messages}')
    msgs = []
    for text in messages:
        msgs.append(TextSendMessage(text=text))
    line_bot_api.reply_message(reply_token, msgs)

def push_message(user, messages):
    logging.debug(f'push_message: user={user} text={messages}')
    msgs = []
    for text in messages:
        msgs.append(TextSendMessage(text=text))
        if len(msgs) >= 5:
            line_bot_api.push_message(user, msgs)
            msgs = []
    line_bot_api.push_message(user, msgs)

def push_image(user, timestamps):
    logging.debug(f'push_image: user={user} timestamp={timestamps}')

    msgs = []
    for timestamp in timestamps:
        imgurl = 'https://' + quote(calculuseal.settings.SERVER_NAME + f'/media/{timestamp}/')
        logging.debug(f'imgurl={imgurl}')
        # TODO: preview image
        msgs.append(ImageSendMessage(original_content_url=imgurl, preview_image_url=imgurl))
        if len(msgs) >= 5:
            # reaching LINE's reply limit
            line_bot_api.push_message(user, msgs)
            msgs = []

    line_bot_api.push_message(user, msgs)

