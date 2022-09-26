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
from LAuth.views import login, signup
from LUserProfile.views import getUserProfile, updateUserProfileField, setupUserProfile, deleteUserProfile


urlpatterns = [         
    path('login', login),
    path('login/', login),
    path("signup", signup),
    path("signup/", signup),
    path('userProfile/getProfile', getUserProfile),
    path('userProfile/getProfile/', getUserProfile),
    path('userProfile/setupProfile', setupUserProfile),
    path('userProfile/setupProfile/', setupUserProfile),
    path('userProfile/updateProfileField', updateUserProfileField),
    path('userProfile/updateProfileField/', updateUserProfileField),
    path('userProfile/deleteProfile', deleteUserProfile),
    path('userProfile/deleteProfile/', deleteUserProfile)

]

