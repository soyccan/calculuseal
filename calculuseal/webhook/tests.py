from django.test import TestCase

from calculuseal import settings

from apis import mathpix
from apis import wolfram

a = mathpix.translate(settings.BASE_DIR + '/tmp/a.jpg')
wolfram.solve(a, settings.BASE_DIR + '/tmp')
