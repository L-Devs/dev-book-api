from datetime import datetime
import email
from genericpath import exists
import http
import json
from lib2to3.pgen2 import token
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .models import UserAuth, User
from datetime import datetime, timedelta
import jwt
import json

# Create your views here.
def login(request):
    if (request.method == "POST"):
        requestBodyUnicode = request.body.decode('utf-8')
        requestBody = json.loads(requestBodyUnicode)
        email = requestBody['email']
        password = requestBody['password']
        

        if (email == None or password == None):
            return HttpResponseBadRequest('No email or password.')   

        user_list = UserAuth.objects.filter(email=email).values_list()
        if(not user_list):
            return JsonResponse({'status': 'Password or username are incorrect'})

        user_list = user_list[0]
        
        DB_userid = user_list[0]
        DB_email = user_list[1]
        DB_password = user_list[2]

        if(email != DB_email or password != DB_password):
            return JsonResponse({'status': 'Password or username are incorrect'})

            
        return generateJWT(requestBody=requestBody)
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

        if (email == "" or password == "" or username == ""):
            return HttpResponseBadRequest("Need all info")
        if UserAuth.objects.filter(email=email).exists():
            return HttpResponseBadRequest("Email Already Used")
        if User.objects.filter(username=username).exists():
            return HttpResponseBadRequest("Username Already Used")


        userauthz = UserAuth(email=email, password=password)
        userauthz.save()

        temp = UserAuth.objects.filter(email=email).values()
        
        usermain = User(userid=temp[0]['userid'], username=username, email=email)    
        usermain.save()

        return generateJWT(requestBody=requestBody)        
    else:
        return HttpResponseBadRequest("not a post request")


def generateJWT(requestBody):
    secret_key = "6e010f75d1c0245a8631cb13371cd9dafcdaa5b3"
    userauthobject = UserAuth.objects.get(email=requestBody['email'])
    userauthobject.token = jwt.encode(payload=requestBody, key=secret_key)
    userauthobject.token_expiration = datetime.now() + timedelta(days = 2)
    userauthobject.save()
    return JsonResponse({"token" : userauthobject.token}, safe=False)
    



