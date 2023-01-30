
# Custom User Model
Custom User Model | [Authenticate with Email](#usage-authentication-with-email)
## Usage (Authentication with Email)
This is a Django project that implements a custom user model using AbstractUser.

#### accounts/models.py
```python
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


```
#### accounts/managers.py
```python
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email,password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

```
#### accounts/signals.py
```python
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models import User,Profile
from django.contrib.auth.models import Group



@receiver(post_save,sender=User)
def User_Profile_group_Creation(sender,instance,created,**kwargs):
    if created:
        user_group,created = Group.objects.get_or_create(name='user')
        instance.groups.add(user_group)
        Profile.objects.create(user = instance)
```
#### settings.py
```python
AUTH_USER_MODEL = 'accounts.User'
```
#### accounts/admin.py
```python
from django.contrib import admin
from accounts.models import User,Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


# Register your models here.

class CustomUserAdmin(BaseUserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','location')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email','get_full_name',  'is_staff')
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)

@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    pass
```
## Features

- Custom User model using AbstractUser
- Sign up with email
- Login with email 
- Profile creation for the user
- User Group creation during sign up

## Requirements

- Python 3.x
- Django 3.x

## Installation

1. Clone the repository:
```python
git clone https://github.com/kavinandan18/coustom-user-model.git
```
2. Change into the project directory:
```python
cd coustom-user-model
```
3. Install the requirements: 
```python
pip install -r requirements.txt
```
4. Run the migrations:
- Makemigrations
```python
python manage.py makemigrations
```
- Migrage
```python
python manage.py migrate
```
5. Create Super user:
```python 
python manage.py createsuperuser
```
6. Run the development server: 
```python
python manage.py runserver
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your branch
5. Create a pull request


