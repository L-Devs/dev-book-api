from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest,HttpResponseNotFound,JsonResponse
import json
from .models import UserInformation

# Create your views here.
def blank(request):
    return HttpResponse("Blank url is working")

@csrf_exempt
def userprofile(request):
    requestDataUnicode = request.body.decode('utf-8') 
    requestData = json.loads(requestDataUnicode)
    if (request.method == 'GET'):
        try:
            userInfoObj = UserInformation.objects.filter(userId=requestData["userId"])
            userInfoObj = userInfoObj.values_list()[0]
            jsonOut = {
                "userId": userInfoObj[0],
                "firstName": userInfoObj[1],
                "lastName":  userInfoObj[2],
                "birthDate":  userInfoObj[3],
                "gender":  userInfoObj[4],
                "phoneNumber":  userInfoObj[5],
                "country":  userInfoObj[6],
            }
        except UserInformation.DoesNotExist:
            return JsonResponse({'status': 'Error', 'description': 'userId does not exist'})
        except KeyError:
            return JsonResponse({'status': 'Error', 'description': 'Please provide a userId'})
        except IndexError as e:
            return JsonResponse({'status': 'Error', 'description': 'User information for this user was not populated correctly', 'verboseError': str(e)})
        except Exception as e:
            return JsonResponse({'status': 'Error', 'description': 'Generic', 'verboseError': str(e)})
        else:
             return JsonResponse({'status': 'Success', 'description': 'Successfully got user the profile information', 'data': jsonOut})

    elif (request.method == "PUT"):
        try:
            userInfoObj = UserInformation.objects.get(userId=requestData["userId"])

            if(requestData["targetField"] == "userId"):
                return JsonResponse({'status': 'Error', 'description': 'You cannot update the value of userId'})

            setattr(userInfoObj, requestData["targetField"], requestData["newValue"])
            userInfoObj.save()
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


        
        


    