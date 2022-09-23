from datetime import datetime
import email
from genericpath import exists
from http.client import BAD_REQUEST, CREATED, INTERNAL_SERVER_ERROR, NOT_FOUND, OK, UNAUTHORIZED
import json
from lib2to3.pgen2 import token
from uuid import uuid4
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .models import User, UserAuth, UserSessions
from datetime import datetime, timedelta
import json

# Create your views here.
def login(request):
    try:
        requestBodyUnicode = request.body.decode('utf-8')
        requestBody = json.loads(requestBodyUnicode)
    except json.JSONDecodeError:
        return JsonResponse ({'status': 'Error', 'message': 'invalid JSON'})
    if (request.method == "POST"):
        try:
            queryResult = UserAuth.objects.filter(email=requestBody['email'])

            # Checking if the filter has found any users with the userId given
            if (not queryResult):
                return JsonResponse({'status': 'Error', 'message': 'email is not registered'}, status=NOT_FOUND)
            
            # Getting the list of data from the query
            dataList = queryResult.values_list()[0]
            
            DB_userid = dataList[0]
            DB_email = dataList[1]
            DB_password = dataList[2]

            if(requestBody['email'] != DB_email or requestBody['password'] != DB_password):
                return JsonResponse({'status': 'Error','message':'Email or password are incorrect'}, status=UNAUTHORIZED)

        except KeyError:
            return JsonResponse({'status': 'Error', 'message': 'Email or password not found in payload'}, status=BAD_REQUEST)   

        except IndexError as e:
            return JsonResponse({'status': 'Error', 'message': 'Authentication information for this user was not populated correctly', 'verboseError': str(e)}, status=INTERNAL_SERVER_ERROR)

        uniqueToken = generateUniqueToken()

        tokenExpiration = datetime.now() + timedelta(days = 2)
        sessionModelObj = UserSessions(token=uniqueToken, tokenExpiration=tokenExpiration, userId=DB_userid)
        sessionModelObj.save()
        response = JsonResponse({'status': 'Success', 'message': 'Logged in'},status=OK)
        response.set_cookie('session_token', uniqueToken, samesite='none', secure=True)   
        return response
    else:
        return JsonResponse({'status': 'Error','message':"This endpoint only supports POST requests"}, status=NOT_FOUND)



#Sign up function

def signup(request):
    #TO-DO:
    # Validate the data and request Filtering (login and signup)
    # Hash passwords
    # Testing
    try:
        requestBodyUnicode = request.body.decode('utf-8')
        requestBody = json.loads(requestBodyUnicode)
    except json.JSONDecodeError:
        return JsonResponse ({'status': 'Error', 'message': 'invalid JSON'})
    if (request.method == "POST"):
        try:
            email = requestBody['email']
            password = requestBody['password']
            username = requestBody['username']

            if UserAuth.objects.filter(email=email).exists():
                return JsonResponse({'status': 'Error', 'message': 'This email is already registered'}, status=UNAUTHORIZED)   
            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': 'Error', 'message': 'This username is already registered'}, status=UNAUTHORIZED)   
        
            authModelObj = UserAuth(email=email, password=password)
            authModelObj.save()

            queryResult = UserAuth.objects.filter(email=email).values('userid')
            queryResult = queryResult[0]
            
            userModelObj = User(userid=queryResult['userid'], username=username, email=email)    
            userModelObj.save()

        except KeyError:
            return JsonResponse({'status': 'Error', 'message': 'Email, password or username not found in payload.'}, status=BAD_REQUEST)   

        uniqueToken = generateUniqueToken()       
                
        tokenExpiration = datetime.now() + timedelta(days = 2)

        DB_sessionObj = UserSessions(token=uniqueToken, tokenExpiration=tokenExpiration, userId=queryResult['userid'])
        DB_sessionObj.save()

        response = JsonResponse({'status': 'Success', 'message': 'Signed up'}, status=CREATED)
        response.set_cookie('session_token', uniqueToken, samesite='none',secure=True)
        return response
    else:
        return JsonResponse({'status': 'Error','message':"This endpoint only supports POST requests"}, status=NOT_FOUND)


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




