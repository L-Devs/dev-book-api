"""dev_book_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from LAuth.views import Login, Signup, devGetUserId
from LUserProfile.views import GetUserProfile, UpdateUserProfileField, SetupUserProfile, DeleteUserProfile
from LPost.views import CreatePost


urlpatterns = [   
    path('devGetUserId', devGetUserId),
    path('devGetUserId/', devGetUserId),
    path('login', Login),
    path('login/', Login),
    path('signup', Signup),
    path('signup/', Signup),
    path('userProfile/getProfile', GetUserProfile),
    path('userProfile/getProfile/', GetUserProfile),
    path('userProfile/setupProfile', SetupUserProfile),
    path('userProfile/setupProfile/', SetupUserProfile),
    path('userProfile/updateProfileField', UpdateUserProfileField),
    path('userProfile/updateProfileField/', UpdateUserProfileField),
    path('userProfile/deleteProfile', DeleteUserProfile),
    path('userProfile/deleteProfile/', DeleteUserProfile),
    path('Post/CreatePost', CreatePost),
    path('Post/CreatePost/', CreatePost)
]

