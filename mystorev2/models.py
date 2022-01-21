from django.db import models
from django.db.models.base import Model
from django.urls import reverse
# Overriden default Django User model by inherit both packages
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, Group
from django.utils.functional import LazyObject


########## MANAGE USER ###########

# Manager for custom User model
class UserManager(BaseUserManager):
    def create_user(self, username, email, group, password=None):
        # Creates and saves a User with the given email and password.
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')
        if not group:
            raise ValueError('Users must have assigned group')

        # normalize the letters to lower case
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password,
            group=group,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # custom User model for creating is_staff user
    def create_staffuser(self, username, email, group, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            group=group,
        )
        user.staff = False
        user.admin = True
        user.is_superuser = False
        user.save(using=self._db)
        return user

    # custom User model for creating superuser user
    def create_superuser(self, username, email, group, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            group=group,
        )
        user.staff = True
        user.admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


########### BASE USER RBAC ############

# Base model custom User model
class User(AbstractBaseUser):
    first_name = models.CharField(verbose_name='first name', max_length=200)
    last_name = models.CharField(verbose_name='last name', max_length=200)
    # group = models.CharField(verbose_name='group', max_length=10)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, null=True, blank=True)
    # required params when creating custom user model
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name='last login', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'group']

    objects = UserManager()

    def __str__(self):
        return self.username

    # only the mandatory functions

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    # @property
    # def is_admin(self):
    #     return self.is_admin

    # def is_superuser(self):
    #     return self.is_superuser


########## WAREHOUSE & PRODUCT MODEL ###########

# Warehouse model
class Warehouse(models.Model):
    wh_name = models.CharField(max_length=200)
    wh_desc = models.CharField(max_length=200)

    def __str__(self):
        return self.wh_name

# Product model


class Product(models.Model):
    prodkey = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    prod_name = models.CharField(max_length=200)
    prod_desc = models.CharField(max_length=200)
    prod_qty = models.IntegerField(default=0)

    def __str__(self):
        return self.prod_name
