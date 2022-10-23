from http.client import BAD_REQUEST, NOT_FOUND, UNAUTHORIZED
import json
from django.http import JsonResponse
from LAuth.views import GetUserId, isTokenValid
from django.shortcuts import render

# Create your views here.
def CreatePost(request):
    try:
        requestBodyUnicode = request.body.decode('utf-8')
        requestBody = json.loads(requestBodyUnicode)
    except json.JSONDecodeError:
        return JsonResponse ({'status': 'Error', 'message': 'invalid JSON'}, status=BAD_REQUEST)

    if (request.method == "POST"):
        if 'session_token' not in request.COOKIES:
            return JsonResponse({'status': 'Error', 'message': 'Failed to authenticate, no session token found in cookies.'}, status=UNAUTHORIZED)

        sessionToken = request.COOKIES['session_token']
        if not isTokenValid(sessionToken):
            return JsonResponse({'status': 'Error', 'message': 'Failed to authenticate, your session is invalid.'}, status=UNAUTHORIZED)
        

        return JsonResponse({'status': GetUserId(sessionToken)})
    else:
        return JsonResponse({'status': 'Error','message':"This endpoint only supports POST requests"}, status=NOT_FOUND)
    pass