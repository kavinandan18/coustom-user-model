from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager





class User(AbstractUser):
    username=None
    email = models.EmailField(_('email address'), unique=True)
    location = models.CharField(max_length=30, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    
    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    
 


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    mobile=models.CharField(max_length=20)
    dob = models.DateField(null=True,blank=True)
    bio = models.CharField(max_length=500,blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)


    def __str__(self) -> str:
        return self.user.get_full_name()
