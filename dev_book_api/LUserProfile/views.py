from http.client import BAD_REQUEST, CREATED, FORBIDDEN, INTERNAL_SERVER_ERROR, NOT_FOUND, OK, UNAUTHORIZED
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json
from .models import LUserProfileModel
from LAuth.views import isTokenValid,getUserId

# Create your views here.


def blank(request):
    return HttpResponse("Blank url is working")


# @csrf_exempt
def setupUserProfile(request):
    try:
        requestBodyUnicode = request.body.decode('utf-8')
        requestBody = json.loads(requestBodyUnicode)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'Error', 'message': 'invalid JSON'}, status=BAD_REQUEST)

    if 'session_token' not in request.COOKIES:
        return JsonResponse({'status': 'Error', 'message': 'Failed to authenticate, no session token found in cookies.'}, status=UNAUTHORIZED)

    sessionToken = request.COOKIES['session_token']
    if not isTokenValid(sessionToken):
        return JsonResponse({'status': 'Error', 'message': 'Failed to authenticate, your session is invalid.'}, status=UNAUTHORIZED)


        
    if (request.method == "POST"):
        try:
            DB_userId = getUserId(sessionToken)
            if DB_userId == -1:
                return JsonResponse({'status': 'Error', 'message': 'Failed to authenticate, your session is invalid.'}, status=UNAUTHORIZED)

            if LUserProfileModel.objects.filter(userId=DB_userId).exists():
                return JsonResponse({'status': 'Error', 'message': 'A user profile for this userId already exists.'}, status=FORBIDDEN)

            userProfileModelObj = LUserProfileModel(
                userId=DB_userId,
                firstName=requestBody["firstName"],
                lastName=requestBody["lastName"],
                birthDate=requestBody["birthDate"],
                gender=requestBody["gender"],
                phoneNumber=requestBody["phoneNumber"],
                country=requestBody["country"]
            )
            userProfileModelObj.save()
            return JsonResponse({'status': 'Success', 'message': 'User profile successfully created.'}, status=CREATED)
        except KeyError:
            return JsonResponse({'status': 'Error', 'message': 'A required field in the payload was not found. Please check the documentation.'}, status=BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'status': 'Error', 'message': 'Unhandled error.', 'verbosError': str(e)}, status=BAD_REQUEST)
    else:
        return JsonResponse({'status': 'Error', 'message': 'This end point only accepts POST requests.'}, status=BAD_REQUEST)


def getUserProfile(request):
    if 'session_token' not in request.COOKIES:
        return JsonResponse({'status': 'Error', 'message': 'Failed to authenticate, no session token found in cookies.'}, status=UNAUTHORIZED)

    sessionToken = request.COOKIES['session_token']
    if not isTokenValid(sessionToken):
        return JsonResponse({'status': 'Error', 'message': 'Failed to authenticate, your session is invalid.'}, status=UNAUTHORIZED)

    if (request.method == 'GET'):
        try:
            DB_userId = getUserId(sessionToken)
            if DB_userId == -1:
                return JsonResponse({'status': 'Error', 'message': 'Failed to authenticate, your session is invalid.'}, status=UNAUTHORIZED)

            queryResult = LUserProfileModel.objects.filter(userId=DB_userId)

            # Checking if the filter has found any users with the userId given
            if (not queryResult):
                return JsonResponse({'status': 'Error', 'message': 'A user profile for this userId does not exist'}, status=NOT_FOUND)

            dataList = queryResult.values_list()[0]

            jsonOut = {
                "firstName": dataList[1],
                "lastName":  dataList[2],
                "birthDate":  dataList[3],
                "gender":  dataList[4],
                "phoneNumber":  dataList[5],
                "country":  dataList[6],
            }


        except LUserProfileModel.DoesNotExist:
            return JsonResponse({'status': 'Error', 'message': 'A user profile for this userId does not exist'}, status=NOT_FOUND)

        except KeyError:
            return JsonResponse({'status': 'Error', 'message': 'userId not found in payload'}, status=BAD_REQUEST)

        except IndexError as e:
            return JsonResponse({'status': 'Error', 'message': 'User information for this user was likely not populated correctly', 'verboseError': str(e)}, status=INTERNAL_SERVER_ERROR)

        except Exception as e:
            return JsonResponse({'status': 'Error', 'message': 'Generic', 'verboseError': str(e)}, status=INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse({'status': 'Success', 'message': 'Successfully got user the profile information', 'data': jsonOut}, status=OK)
    else:
        return JsonResponse({'status': 'Error', 'message': 'This end point only accepts GET requests.'}, status=BAD_REQUEST)


def updateUserProfileField(request):
    try:
        requestBodyUnicode = request.body.decode('utf-8')
        requestBody = json.loads(requestBodyUnicode)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'Error', 'message': 'invalid JSON'}, status=BAD_REQUEST)

    if 'session_token' not in request.COOKIES:
        return JsonResponse({'status': 'Error', 'message': 'Failed to authenticate, no session token found in cookies.'}, status=UNAUTHORIZED)

    sessionToken = request.COOKIES['session_token']
    if not isTokenValid(sessionToken):
        return JsonResponse({'status': 'Error', 'message': 'Failed to authenticate, your session is invalid.'}, status=UNAUTHORIZED)

    if (request.method == "PUT"):
        try:
            DB_userId = getUserId(sessionToken)
            if DB_userId == -1:
                return JsonResponse({'status': 'Error', 'message': 'Failed to authenticate, your session is invalid.'}, status=UNAUTHORIZED)

            queryResult = LUserProfileModel.objects.get(userId=DB_userId)

            if (requestBody["targetField"] == "userId"):
                return JsonResponse({'status': 'Error', 'message': 'You cannot update the value of \'userId\''}, status=FORBIDDEN)

            setattr(queryResult,
                    requestBody["targetField"], requestBody["newValue"])
            queryResult.save()
            return JsonResponse({'status': 'Success', 'message': 'Successfully updated the field ' + requestBody["targetField"]}, status=CREATED)

        except LUserProfileModel.DoesNotExist:
            return JsonResponse({'status': 'Error', 'message': 'A user profile for this userId does not exist'}, status=NOT_FOUND)

        except KeyError:
            return JsonResponse({'status': 'Error', 'message': 'userId, targetField or newValue not found in payload'}, status=BAD_REQUEST)

        except Exception as e:
            return JsonResponse({'status': 'Error', 'message': 'Missing userId, targetField or newValue'}, status=BAD_REQUEST)

    else:
        return JsonResponse({'status': 'Error', 'message': 'This end point only accepts PUT requests.'}, status=BAD_REQUEST)


def deleteUserProfile(request):
    if 'session_token' not in request.COOKIES:
        return JsonResponse({'status': 'Error', 'message': 'Failed to authenticate, no session token found in cookies.'}, status=UNAUTHORIZED)

    sessionToken = request.COOKIES['session_token']
    if not isTokenValid(sessionToken):
        return JsonResponse({'status': 'Error', 'message': 'Failed to authenticate, your session is invalid.'}, status=UNAUTHORIZED)

    if request.method == "DELETE":

        try:
            DB_userId = getUserId(sessionToken)
            if DB_userId == -1:
                return JsonResponse({'status': 'Error', 'message': 'Failed to authenticate, your session is invalid.'}, status=UNAUTHORIZED)

            queryResult = LUserProfileModel.objects.get(userId=DB_userId)
            queryResult.delete()

            return JsonResponse({'status': 'Success', 'message': 'User profile successfully deleted'}, status=OK)

        except KeyError:
            return JsonResponse({'status': 'Error', 'message': 'userId was not found in the payload.'}, status=BAD_REQUEST)

        except LUserProfileModel.DoesNotExist:
            return JsonResponse({'status': 'Error', 'message': 'A user profile for this userId does not exist'}, status=NOT_FOUND)

    else:
        return JsonResponse({'status': 'Error', 'message': 'This end point only accepts DELETE requests.'}, status=BAD_REQUEST)
