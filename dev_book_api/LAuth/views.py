from datetime import datetime
import json
from lib2to3.pgen2 import token
from django.http import HttpResponse, HttpResponseBadRequest
import requests
from .models import UserAuth, User
from datetime import datetime, timedelta


# Create your views here.
def login(request):
    if (request.method == "POST"):
        requestBodyUnicode = request.body.decode('utf-8')
        requestBody = json.loads(requestBodyUnicode)
        email = requestBody['email']
        password = requestBody['password']

        if (email == None or password == None):
            return HttpResponseBadRequest('No email or password.')   

    else:
        return HttpResponseBadRequest("not a post request")



#Sign up function

def signup(request):
    #TO-DO:
    # Validation
    # hash password
    # idk
    if (request.method == "POST"):
        requestBodyUnicode = request.body.decode('utf-8')
        requestBody = json.loads(requestBodyUnicode)
        email = requestBody['email']
        password = requestBody['password']
        username = requestBody['username']
        token = requestBody['token']
        token_expiration = datetime.now() + timedelta(days = 2)
        if (email == None or password == None or username == None):
            return HttpResponseBadRequest("Signup Failed")
        else:
            userauthz = UserAuth(username=username, password=password, token=token, token_expiration=token_expiration)
            userauthz.save()

            temp = UserAuth.objects.filter(username=username).values()
            
            usermain = User(userid=temp[0]['userid'], username=username, email=email)    
            usermain.save()

            usersAuth_list = UserAuth.objects.all()
            usersMain_list = User.objects.all()
            return HttpResponse(usersAuth_list.values_list())          
    else:
        return HttpResponseBadRequest("not a post request")

