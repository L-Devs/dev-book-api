from django.views.decorators.csrf import csrf_exempt
import re
from urllib.error import HTTPError
from wsgiref.simple_server import WSGIRequestHandler

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest,HttpResponseNotFound,JsonResponse

from django.core.serializers.json import DjangoJSONEncoder
import json
import datetime

# Create your views here.
def blank(request):
    return HttpResponse("Blank url is working")

@csrf_exempt
def userinfo(request):
    obj = {
        "firstName" : "joe",
        "lastName" : "biden",
        "age" : 69,
        "phoneNumber" : 31232,
        "dateOfBirth" : datetime.datetime(1966, 12, 22), 
        "gender" : "non binary", 
        "country" : "USA"
    }
    username= "Mosudani"
    if (request.method == 'GET'):
        json_str = json.dumps(obj , cls=DjangoJSONEncoder)
        if (username == obj.get("firstName")):
            return HttpResponse(json_str)
        else:
            return HttpResponseNotFound("Not Found")
        
    elif (request.method == "PUT"):
        # check if user is authenticated
        requestDataUnicode = request.body.decode('utf-8') 
        requestData = json.loads(requestDataUnicode)
        obj["firstName"] = requestData["firstName"]
        obj["age"] = requestData["age"]
        json_str = json.dumps(obj , cls=DjangoJSONEncoder)
        return HttpResponse(json_str)

    elif(request.method == 'POST'):
        jsondata = json.loads(request.body)
        Username = jsondata["Username"]
        FirstName = jsondata["FirstName"]
        LastName = jsondata["LastName"]
        Age = jsondata["Age"]
        PhoneNumber = jsondata["PhoneNumber"]
        DateofBirth= jsondata["DateofBirth"]
        Gender = jsondata["Gender"]
        Country = jsondata["Country"]
        if(Username == None):
             return HttpResponseBadRequest("Username not provided")
        elif(FirstName == None):
            return HttpResponseBadRequest("First name not provided")
        elif(LastName == None):
            return HttpResponseBadRequest("Last name not provided")
        elif(Age == None):
            return HttpResponseBadRequest("Age not provided")
        elif(PhoneNumber == None):
            return HttpResponseBadRequest("Phone number not provided")
        elif(DateofBirth == None):
            return HttpResponseBadRequest("Date of birth not provided")
        elif(Gender == None):
            return HttpResponseBadRequest("Gender not provided")
        elif(Country == None):
            return HttpResponseBadRequest("Country not provided")
        # print(jsondata["username"])
    return JsonResponse(jsondata) 


        
        


    