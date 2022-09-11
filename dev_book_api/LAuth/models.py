from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
# class UserManager(BaseUserManager):
#     def create_user(self, userid, email, username):
#         if not email:
#             raise ValueError('user must have email')
#         if not username:
#             raise ValueError('user must have username')

#         user = self.model(
#             userid=userid,
#             email=self.normalize_email(email),
#             username=username,
#         )
#         user.save()
#         return user

#     def create_superuser(self, email, username):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             username=username
#         )
#         user.is_staff = True
#         user.is_superuser = True
#         user.save()
#         return user


class User(models.Model):

    #Fields
    userid = models.IntegerField(primary_key=True,unique=True)
    email = models.EmailField(verbose_name='email', unique=True)
    username = models.CharField(verbose_name='username', max_length=255, unique=True)


    #objects = UserManager()
    class Meta:
        db_table = "User"

    def __str__(self) -> str:
        return self.username


class UserAuth(models.Model):
    userid = models.IntegerField(primary_key=True,unique=True)
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    password = models.CharField(verbose_name='password', max_length=255)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "UserAuthentication"

    def __str__(self) -> str:
        return self.email

class UserSessions(models.Model):
    token = models.CharField(primary_key=True, unique=True,verbose_name='token', max_length=255)
    tokenExpiration = models.DateTimeField(verbose_name='tokenExpiration')
    userId = models.IntegerField(verbose_name='userid')

    class Meta:
        db_table = "UserSessions"

    def __str__(self) -> str:
        return self.userid
