from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def webhook(request):
    return HttpResponse("HI I'M CALCULUSEAL")
