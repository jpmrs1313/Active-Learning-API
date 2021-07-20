from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Deve ter um email')
        
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)

        user.set_password(password)
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin): 
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=False, default=" ")
    last_name = models.CharField(max_length=255, null=False, default=" ")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_medic = models.BooleanField(default=False)
    is_specialist = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email