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
                return JsonResponse({'status': 'Error', 'description': 'userId does not exist'})

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
            return JsonResponse({'status': 'Error', 'description': 'Please provide a userId'})

        except IndexError as e:
            return JsonResponse({'status': 'Error', 'description': 'User information for this user was likely not populated correctly', 'verboseError': str(e)})
            
        except Exception as e:
            return JsonResponse({'status': 'Error', 'description': 'Generic', 'verboseError': str(e)})
        else:
             return JsonResponse({'status': 'Success', 'description': 'Successfully got user the profile information', 'data': jsonOut})

    elif (request.method == "PUT"):
        try:
            queryResult = LUserProfileModel.objects.get(userId=requestData["userId"])
        
            if(requestData["targetField"] == "userId"):
                return JsonResponse({'status': 'Error', 'description': 'You cannot update the value of userId'})

            setattr(queryResult, requestData["targetField"], requestData["newValue"])
            queryResult.save()
            return JsonResponse({'status': 'Success','description': 'Successfully updated the field ' + requestData["targetField"]})
        except Exception as e:
            return JsonResponse({'status': 'Error', 'description': 'Missing userId, targetField or newValue'})

    elif(request.method == 'POST'):
        return JsonResponse({'status': 'Error', 'description': 'Generic'})
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


        
        


    