from django.db import models
import random

chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


def key_gen():
    password = ''

    for i in range(10):
        password += random.choice(chars)

    return password


class KodeUser(models.Model):
    id = models.AutoField('id', primary_key=True, auto_created=True)
    username = models.CharField('username', max_length=100, unique=True)
    email = models.CharField('email', max_length=100, blank=True)
    password = models.TextField('password', blank=True)
    invitation_code = models.TextField('invitation_code', default=key_gen)

    def __str__(self):
        return 'Name - {0}, Email - {1}, UserType - {2}'.format(
            self.username,
            self.email,
            self.invitation_code)


class Test(models.Model):
    col = models.CharField(max_length=10)
