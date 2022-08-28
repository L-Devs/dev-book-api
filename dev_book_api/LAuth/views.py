from datetime import datetime
import email
import json
from lib2to3.pgen2 import token
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
import requests
from .models import UserAuth, User
from datetime import datetime, timedelta
import jwt
import json

# Create your views here.
def login(request):
    if (request.method == "POST"):
        requestBodyUnicode = request.body.decode('utf-8')
        requestBody = json.loads(requestBodyUnicode)
        

        if (requestBody['email'] == None or requestBody['password'] == None):
            return HttpResponseBadRequest('No email or password.')
        secret_key = "6e010f75d1c0245a8631cb13371cd9dafcdaa5b3"
        try:
            uservalues = User.objects.filter(email=requestBody['email']).values()
            userauthvalues = UserAuth.objects.filter(userid=uservalues[0]['userid']).values()
            if (uservalues[0]['email'] == requestBody['email'] and userauthvalues[0]['password']):
                userauthobject = UserAuth.objects.get(userid=uservalues[0]['userid'])
                userauthobject.token = jwt.encode(payload=requestBody, key=secret_key)
                userauthobject.token_expiration = datetime.now() + timedelta(days = 2)
                userauthobject.save()
                return JsonResponse({"token" : userauthobject.token}, safe=False)
        except:
           return HttpResponseBadRequest("Email isn't in database")
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

        if (email == None or password == None or username == None):
            return HttpResponseBadRequest("Signup Failed")
        else:
            userauthz = UserAuth(email=email, password=password)
            userauthz.save()

            temp = UserAuth.objects.filter(email=email).values()
            
            usermain = User(userid=temp[0]['userid'], username=username, email=email)    
            usermain.save()

            usersAuth_list = UserAuth.objects.all()
            usersMain_list = User.objects.all()
            return HttpResponse(usersAuth_list.values_list())          
    else:
        return HttpResponseBadRequest("not a post request")

