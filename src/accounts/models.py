from django.db import models
from django.urls import reverse
from django.utils.encoding import smart_text
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
from django.db.models.signals import post_save


USERNAME_REGEX="^[a-zA-Z0-9_.]*$"


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):

        """
        Creates and saves a User with the given username,email and password.
        """

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        
        """
        Creates and saves a User with the given username,email and password.
        """

        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUserModel(AbstractBaseUser):

    username        = models.CharField(

                                        max_length=120,
                                        validators=[RegexValidator(
                                                regex=USERNAME_REGEX,
                                                message="Username must be Alphanumeric or contain any of the follwoing : '_ .'",
                                                code="Invalid Username"
                                            )],
                                        unique=True
                                    )
    email           = models.EmailField(
                                        verbose_name='Email address',
                                        max_length=255,
                                        unique=True,
                                    )

    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False,blank=True)
    is_admin        = models.BooleanField(default=False,blank=True)

    objects         = UserManager()

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True



class GuestEmail(models.Model):
    email           = models.EmailField()
    active          = models.BooleanField(default=True)
    updated         = models.DateTimeField(auto_now=True)
    timestamp       = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.email