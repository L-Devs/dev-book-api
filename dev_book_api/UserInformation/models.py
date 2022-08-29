from django.db import models
from django_countries.fields import CountryField

# Create your models here.

class UserInformation(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    userId = models.IntegerField(primary_key=True,unique=True)
    firstName = models.CharField(verbose_name='firstname', max_length=255)
    lastName = models.CharField(verbose_name='lastname', max_length=255)
    birthDate = models.DateField(verbose_name='birthdate', null = True, blank= True) 
    gender = models.CharField(verbose_name='gender',max_length=1, choices=GENDER_CHOICES)
    phoneNumber = models.CharField(verbose_name='phone', max_length=15)
    country = CountryField(verbose_name='country')
    
    def calculate_age(self):
        import datetime
        return int((datetime.date.today() - self.birth_date).days / 365.25)

    
    class Meta:
        db_table = "UserInformation"

    def __str__(self) -> str:
        return self.first_name