from django.http import HttpResponse, HttpResponseBadRequest
import requests

# Create your views here.
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    if (email == None or password == None):
        return HttpResponseBadRequest('No email or password.')
    return HttpResponse('signed in with:'+email)


#Sign up function

def signup(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    username = request.POST.get("username")
    if (email == None or password == None or username == None):
        return HttpResponseBadRequest("Signup Failed")
    return HttpResponse("Sign up successful!:"+username)