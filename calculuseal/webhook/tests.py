from django.test import TestCase

import logging

from calculuseal import settings
from apis import mathpix
from apis import wolfram
from webhook import views

logging.basicConfig(level='DEBUG', format='[%(levelname)s] file=%(pathname)s; %(message)s')

# a = mathpix.translate(settings.BASE_DIR + '/media/_in.jpg')
# wolfram.solve(a, settings.BASE_DIR + '/media')
# views.reply_image('444', '/home/soyccan/calculuseal/calculuseal/static/media/55/a.jpg')
open(settings.BASE_DIR + '/static/media/testrw', 'w').write('wonderful')

