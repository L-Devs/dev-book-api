from django.http import HttpResponse
from django.shortcuts import render
import requests

# Create your views here.
def login(request):
    email = request.GET.get('email')
    password = request.GET.get('password')
    return HttpResponse('signed in with:'+email)