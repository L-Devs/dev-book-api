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
    email = models.EmailField(verbose_name='email', unique=True)
    username = models.CharField(verbose_name='username', max_length=70, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Unique Identifier (what to login with)
    USERNAME_FIELD = 'email'

    # Required Fields to make a user object besides the unique identifier and password
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    def has_module_perms(self, app_label):
        return True


class Persons(models.Model):
    PersonID = models.IntegerField(default=0)
    LastName = models.CharField(max_length=255)
    FirstName = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    City = models.CharField(max_length=255)

    def __str__(self):
        return self.name


