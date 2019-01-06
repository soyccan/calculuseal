import logging
import json

from django.test import TestCase
from django.http import HttpRequest

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage
)


from calculuseal import settings
from apis import mathpix
from apis import wolfram
from webhook import views




def solve_test():
  wolfram.solve('4x^5 +x^3 +2x+4=0')

def web_request_test():
  r = HttpRequest()
  r.__dict__.update({
      "COOKIES": {},
      "META": {
        "CONTENT_LENGTH": "283",
        "CONTENT_TYPE": "application/json;charset=UTF-8",
        "HTTP_ACCEPT": "*/*",
        "HTTP_CONNECTION": "close",
        "HTTP_CONNECT_TIME": "0",
        "HTTP_HOST": "calculuseal.herokuapp.com",
        "HTTP_TOTAL_ROUTE_TIME": "0",
        "HTTP_USER_AGENT": "LineBotWebhook/1.0",
        "HTTP_VIA": "1.1 vegur",
        "HTTP_X_FORWARDED_FOR": "203.104.146.155",
        "HTTP_X_FORWARDED_PORT": "443",
        "HTTP_X_FORWARDED_PROTO": "https",
        "HTTP_X_LINE_SIGNATURE": "hmepvS++l30sdOOow7/qoZMQSencI0eifx56akSQvkw=",
        "HTTP_X_REQUEST_ID": "7414498e-1a10-42f3-bcf5-5ed187668d48",
        "HTTP_X_REQUEST_START": "1546502440767",
        "PATH_INFO": "/webhook",
        "QUERY_STRING": "",
        "RAW_URI": "/webhook",
        "REMOTE_ADDR": "10.61.183.62",
        "REMOTE_PORT": "33931",
        "REQUEST_METHOD": "POST",
        "SCRIPT_NAME": "",
        "SERVER_NAME": "0.0.0.0",
        "SERVER_PORT": "44084",
        "SERVER_PROTOCOL": "HTTP/1.1",
        "SERVER_SOFTWARE": "gunicorn/19.9.0",
        # "gunicorn.socket": "<socket.socket fd=10, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=(\"172.17.204.30\", 44084), raddr=(\"10.61.183.62\", 33931)>",
        # "wsgi.errors": "<gunicorn.http.wsgi.WSGIErrorsWrapper object at 0x7f23ce080eb8>",
        # "wsgi.file_wrapper": "<class \"gunicorn.http.wsgi.FileWrapper\">",
        # "wsgi.input": "<gunicorn.http.body.Body object at 0x7f23ce080da0>",
        # "wsgi.multiprocess": True,
        # "wsgi.multithread": False,
        # "wsgi.run_once": False,
        # "wsgi.url_scheme": "https",
        # "wsgi.version": "(1, 0)"
      },
      "_encoding": "UTF-8",
      "_messages": "<django.contrib.messages.storage.fallback.FallbackStorage object at 0x7f23ce0cb668>",
      "_post_parse_error": False,
      "_read_started": False,
      "_stream": "<django.core.handlers.wsgi.LimitedStream object at 0x7f23ce0cb080>",
      "content_params": {
        "charset": "UTF-8"
      },
      "content_type": "application/json",
      "environ": {
        "CONTENT_LENGTH": "283",
        "CONTENT_TYPE": "application/json;charset=UTF-8",
        "HTTP_ACCEPT": "*/*",
        "HTTP_CONNECTION": "close",
        "HTTP_CONNECT_TIME": "0",
        "HTTP_HOST": "calculuseal.herokuapp.com",
        "HTTP_TOTAL_ROUTE_TIME": "0",
        "HTTP_USER_AGENT": "LineBotWebhook/1.0",
        "HTTP_VIA": "1.1 vegur",
        "HTTP_X_FORWARDED_FOR": "203.104.146.155",
        "HTTP_X_FORWARDED_PORT": "443",
        "HTTP_X_FORWARDED_PROTO": "https",
        "HTTP_X_LINE_SIGNATURE": "hmepvS++l30sdOOow7/qoZMQSencI0eifx56akSQvkw=",
        "HTTP_X_REQUEST_ID": "7414498e-1a10-42f3-bcf5-5ed187668d48",
        "HTTP_X_REQUEST_START": "1546502440767",
        "PATH_INFO": "/webhook",
        "QUERY_STRING": "",
        "RAW_URI": "/webhook",
        "REMOTE_ADDR": "10.61.183.62",
        "REMOTE_PORT": "33931",
        "REQUEST_METHOD": "POST",
        "SCRIPT_NAME": "",
        "SERVER_NAME": "0.0.0.0",
        "SERVER_PORT": "44084",
        "SERVER_PROTOCOL": "HTTP/1.1",
        "SERVER_SOFTWARE": "gunicorn/19.9.0",
        # "gunicorn.socket": "<socket.socket fd=10, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('172.17.204.30', 44084), raddr=('10.61.183.62', 33931)>",
        # "wsgi.errors": "<gunicorn.http.wsgi.WSGIErrorsWrapper object at 0x7f23ce080eb8>",
        # "wsgi.file_wrapper": "<class gunicorn.http.wsgi.FileWrapper>",
        # "wsgi.input": "<gunicorn.http.body.Body object at 0x7f23ce080da0>",
        # "wsgi.multiprocess": True,
        # "wsgi.multithread": False,
        # "wsgi.run_once": False,
        # "wsgi.url_scheme": "https",
        # "wsgi.version": "(1, 0)"
      },
      "method": "POST",
      "path": "/webhook",
      "path_info": "/webhook",
      # "resolver_match": "ResolverMatch(func=webhook.views.webhook, args=(), kwargs={}, url_name=None, app_names=[], namespaces=[])",
      # "session": "<django.contrib.sessions.backends.db.SessionStore object at 0x7f23ce0cb0b8>",
      # "user": "<SimpleLazyObject: <function AuthenticationMiddleware.process_request.<locals>.<lambda> at 0x7f23ce078d08>>"
    })
  r._body = json.JSONEncoder().encode(
  {
      "destination": "Ude33b927cb5eb14ee3c89e4076a611b3",
      "events": [
          {
              "message": {
                  "id": "9119085696777",
                  "text": "aaabb",
                  "type": "text"
              },
              "replyToken": "7e3e965eac184553930b7019c9479ec7",
              "source": {
                  "type": "user",
                  "userId": "U7c2232b80dc0104731e13349fb24c6d7"
              },
              "timestamp": 1546703413000,
              "type": "message"
          },
          {
              "message": {
                  "id": "9119085999999",
                  "type": "image",
                  "contentProvider.type": "line",
                  "contentProvider.originalContentUrl": "https://i.imgur.com/iiVJJ4A.jpg",
                  "contentProvider.previewImageUrl": "https://i.imgur.com/iiVJJ4A.jpg",
              },
              "replyToken": "7e3e965eac184553930b7019c9479ec7",
              "source": {
                  "type": "user",
                  "userId": "U7c2232b80dc0104731e13349fb24c6d7"
              },
              "timestamp": 1546703413000,
              "type": "message"
          }
      ]
  }).encode()
  views.webhook(r)

# a = mathpix.translate(settings.BASE_DIR + '/media/_in.jpg')
# wolfram.solve(a, settings.BASE_DIR + '/media')
# views.reply_image('444', '/home/soyccan/calculuseal/calculuseal/static/media/55/a.jpg')
# open(settings.BASE_DIR + '/static/media/testrw', 'w').write('wonderful')

