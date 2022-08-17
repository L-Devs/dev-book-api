from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('user must have email')
        if not username:
            raise ValueError('user must have username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):

    #Fields
    userid = models.IntegerField(primary_key=True,unique=True)
    email = models.EmailField(verbose_name='email', unique=True)
    username = models.CharField(verbose_name='username', max_length=255, unique=True)

    # is_superuser = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)

    # Unique Identifier (what to login with)
    USERNAME_FIELD = 'username'

    # Required Fields to make a user object besides the unique identifier and password
    REQUIRED_FIELDS = ['email']
    

    objects = UserManager()
    class Meta:
        db_table = "Users"

    def __str__(self) -> str:
        return self.username


class UserAuth(models.Model):
    userid = models.IntegerField(primary_key=True,unique=True)
    username = models.CharField(verbose_name='username', max_length=255, unique=True)
    password = models.CharField(verbose_name='password', max_length=255)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "UserAuthentication"

    def __str__(self) -> str:
        return self.username