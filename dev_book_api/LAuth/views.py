from lib2to3.pgen2.parse import ParseError
from types import NoneType
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

import requests

# Create your views here.
def login(request):
    email = request.GET.get('email')
    password = request.GET.get('password')
    if (email == None or password == None):
        return HttpResponseBadRequest('No email or password.')
    return HttpResponse('signed in with:'+email)


#Sign up function

def signup(request):
    email = request.GET.get("email")
    password = request.GET.get("password")
    username = request.GET.get("username")
    if (email == None or password == None or username == None):
        return HttpResponseBadRequest("Signup Failed")
    return HttpResponse("Sign up successful!:"+username)