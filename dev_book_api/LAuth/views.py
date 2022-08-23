import json
from django.http import HttpResponse, HttpResponseBadRequest
import requests
from .models import UserAuth, User

# Create your views here.
def login(request):
    if (request.method == 'POST'):
        jsondata = json.loads(request.body)
        email = jsondata['email']
        password = jsondata['password']
        if (email == None or password == None):
            return HttpResponseBadRequest('No email or password.')
    return HttpResponse('signed in with:'+email)


#Sign up function

def signup(request):
    #TO-DO:
    # Validation
    # hash password
    # add to User table
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
            userauthz = UserAuth(username=username, password=password)
            #usermain = User(userid= userauthz.userid, username=username, email=email, password=password)
            userauthz.save()
            #usermain.save()
            usersAuth_list = UserAuth.objects.all()
            #usersMain_list = User.objects,all()
            return HttpResponse(usersAuth_list.values_list())          
    else:
        return HttpResponseBadRequest("not a post request")