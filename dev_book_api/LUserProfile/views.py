from http.client import BAD_REQUEST, CREATED, FORBIDDEN, INTERNAL_SERVER_ERROR, NOT_FOUND, OK
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
import json
from .models import LUserProfileModel

# Create your views here.
def blank(request):
    return HttpResponse("Blank url is working")

@csrf_exempt
def userprofile(request):
    requestDataUnicode = request.body.decode('utf-8') 
    requestData = json.loads(requestDataUnicode)
    if (request.method == 'GET'):
        try:
            queryResult = LUserProfileModel.objects.filter(userId=requestData["userId"])

            # Checking if the filter has found any users with the userId given
            if (not queryResult):
                return JsonResponse({'status': 'Error', 'message': 'userId does not exist'}, status=NOT_FOUND)

            dataList = queryResult.values_list()[0]
            
            jsonOut = {
                "userId": dataList[0],
                "firstName": dataList[1],
                "lastName":  dataList[2],
                "birthDate":  dataList[3],
                "gender":  dataList[4],
                "phoneNumber":  dataList[5],
                "country":  dataList[6],
            }

        except KeyError:
            return JsonResponse({'status': 'Error', 'message': 'userId not found in payload'}, status=BAD_REQUEST)

        except IndexError as e:
            return JsonResponse({'status': 'Error', 'message': 'User information for this user was likely not populated correctly', 'verboseError': str(e)}, status=INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return JsonResponse({'status': 'Error', 'message': 'Generic', 'verboseError': str(e)}, status=INTERNAL_SERVER_ERROR)
        else:
             return JsonResponse({'status': 'Success', 'message': 'Successfully got user the profile information', 'data': jsonOut}, status=OK)

    elif (request.method == "PUT"):
        try:
            queryResult = LUserProfileModel.objects.get(userId=requestData["userId"])
        
            if(requestData["targetField"] == "userId"):
                return JsonResponse({'status': 'Error', 'message': 'You cannot update the value of \'userId\''}, status=FORBIDDEN)

            setattr(queryResult, requestData["targetField"], requestData["newValue"])
            queryResult.save()
            return JsonResponse({'status': 'Success','message': 'Successfully updated the field ' + requestData["targetField"]}, status=CREATED)
        except Exception as e:
            return JsonResponse({'status': 'Error', 'message': 'Missing userId, targetField or newValue'}, status=BAD_REQUEST)

    elif(request.method == 'POST'):
        return JsonResponse({'status': 'Error', 'message': 'Generic'}, status=BAD_REQUEST)
        # Okkio: TEMPORARILY OFF TO BE REVIEWD
    #     jsondata = json.loads(request.body)
    #     Username = jsondata["Username"]
    #     FirstName = jsondata["FirstName"]
    #     LastName = jsondata["LastName"]
    #     Age = jsondata["Age"]
    #     PhoneNumber = jsondata["PhoneNumber"]
    #     DateofBirth= jsondata["DateofBirth"]
    #     Gender = jsondata["Gender"]
    #     Country = jsondata["Country"]
    #     if(Username == None):
    #          return HttpResponseBadRequest("Username not provided")
    #     elif(FirstName == None):
    #         return HttpResponseBadRequest("First name not provided")
    #     elif(LastName == None):
    #         return HttpResponseBadRequest("Last name not provided")
    #     elif(Age == None):
    #         return HttpResponseBadRequest("Age not provided")
    #     elif(PhoneNumber == None):
    #         return HttpResponseBadRequest("Phone number not provided")
    #     elif(DateofBirth == None):
    #         return HttpResponseBadRequest("Date of birth not provided")
    #     elif(Gender == None):
    #         return HttpResponseBadRequest("Gender not provided")
    #     elif(Country == None):
    #         return HttpResponseBadRequest("Country not provided")
    #     # print(jsondata["username"])
    # return JsonResponse(jsondata)


        
        


    