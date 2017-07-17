from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.


class AccountManager(BaseUserManager):

    def create_user(self, username, nickname=None, password=None):
        if not username:
            raise ValueError('User must have username')

        user = self.model(
            username=username,
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, nickname, password):
        user = self.create_user(
            username=username,
            nickname=nickname,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username = models.CharField(max_length=128, unique=True)
    nickname = models.CharField(max_length=256)
    avatar = models.ImageField(blank=True)
    address = models.CharField(max_length=1024, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    register_date = models.DateTimeField(auto_now_add=True, blank=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return True
