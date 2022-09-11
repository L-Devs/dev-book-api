from datetime import datetime
import email
from genericpath import exists
import json
from lib2to3.pgen2 import token
from uuid import uuid4
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .models import User, UserAuth, UserSessions
from datetime import datetime, timedelta
import jwt
import json

# Create your views here.
def login(request):
    requestBodyUnicode = request.body.decode('utf-8')
    requestBody = json.loads(requestBodyUnicode)
    if (request.method == "POST"):
        try:
            queryResult = UserAuth.objects.filter(email=requestBody['email'])

            # Checking if the filter has found any users with the userId given
            if (not queryResult):
                return JsonResponse({'status': 'Error', 'description': 'userId does not exist'})
            
            # Getting the list of data from the query
            dataList = queryResult.values_list()[0]
            
            DB_userid = dataList[0]
            DB_email = dataList[1]
            DB_password = dataList[2]

            if(requestBody['email'] != DB_email or requestBody['password'] != DB_password):
                return JsonResponse({'status': 'Password or username are incorrect'})

        except KeyError:
            return JsonResponse({'status': 'Error', 'description': 'Please provide an email'})   

        except IndexError as e:
            return JsonResponse({'status': 'Error', 'description': 'Authentication information for this user was not populated correctly', 'verboseError': str(e)})

        uniqueToken = generateUniqueToken()

        tokenExpiration = datetime.now() + timedelta(days = 2)
        sessionModelObj = UserSessions(token=uniqueToken, tokenExpiration=tokenExpiration, userId=DB_userid)
        sessionModelObj.save()

        return JsonResponse({'status': 'Success', 'description': 'Logged in','token':uniqueToken})
    else:
        return HttpResponseBadRequest("not a post request")



#Sign up function

def signup(request):
    #TO-DO:
    # Validation
    # hash password
    # idk
    requestBodyUnicode = request.body.decode('utf-8')
    requestBody = json.loads(requestBodyUnicode)
    if (request.method == "POST"):
        try:
            email = requestBody['email']
            password = requestBody['password']
            username = requestBody['username']

            if UserAuth.objects.filter(email=email).exists():
                return JsonResponse({'status': 'Error', 'description': 'This email is already registered'})   
            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': 'Error', 'description': 'This username is already registered'})   
        
            authModelObj = UserAuth(email=email, password=password)
            authModelObj.save()

            queryResult = UserAuth.objects.filter(email=email).values('userid')
            queryResult = queryResult[0]
            
            userModelObj = User(userid=queryResult['userid'], username=username, email=email)    
            userModelObj.save()

        except KeyError:
            return JsonResponse({'status': 'Error', 'description': 'Please provide an email, password and username.'})   

        uniqueToken = generateUniqueToken()       
                
        tokenExpiration = datetime.now() + timedelta(days = 2)

        DB_sessionObj = UserSessions(token=uniqueToken, tokenExpiration=tokenExpiration, userId=queryResult['userid'])
        DB_sessionObj.save()

        return JsonResponse({'status': 'Success', 'description': 'Signed up','token':uniqueToken})     
    else:
        return HttpResponseBadRequest("not a post request")


def generateUniqueToken():
    newToken = uuid4()

    # Checking if the newly generated token is unique
    notUnique = True
    while notUnique:
        existingTokenObj = UserSessions.objects.filter(token=newToken)
        if(not existingTokenObj):
            notUnique = False
        else:
            newToken = uuid4()
    return newToken




