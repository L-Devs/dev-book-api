from urllib.error import HTTPError
from wsgiref.simple_server import WSGIRequestHandler
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.core.serializers.json import DjangoJSONEncoder
import json
import datetime

# Create your views here.
def blank(request):
    return HttpResponse("Blank url is working")

def userinfo(request, username):
    obj = {
        "firstName" : "joe",
        "lastName" : "biden",
        "age" : 69,
        "phoneNumber" : 31232,
        "dateOfBirth" : datetime.datetime(1966, 12, 22), 
        "gender" : "non binary", 
        "country" : "USA"
    }
    json_str = json.dumps(obj , cls=DjangoJSONEncoder)
    if (username == obj.get("firstName")):
        return HttpResponse(json_str)
    else:
        return HttpResponseNotFound("Not Found")

    