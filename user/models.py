from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, id, password, nickname):
        if not id:
            raise ValueError('Users must have an id')
        if not nickname:
            raise ValueError('Users must have a nickname')

        user = self.model(
            id = id,
            nickname = nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, password, nickname):
        user = self.create_user(
            id = id,
            password = password,
            nickname = nickname,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.nickname
