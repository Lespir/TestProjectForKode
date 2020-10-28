from django.db import models
import random

chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


def key_gen():
    password = ''

    for i in range(10):
        password += random.choice(chars)

    return password


class Manager(models.Model):
    id = models.AutoField('id', primary_key=True, auto_created=True)
    username = models.CharField('username', max_length=50, unique=True)
    nickname = models.CharField('nickname', max_length=50, blank=True)
    email = models.CharField('email', max_length=100, blank=True)
    password = models.TextField('password', blank=True)
    invitation_code = models.CharField('invitation_code', max_length=11, default=key_gen)

    def __str__(self):
        return 'Name - {0}, Email - {1}, Invitation Code - {2}'.format(self.username, self.email, self.invitation_code)


class Product(models.Model):
    image = models.TextField('image', null=True, blank=True, default='https://mega.nz/file/389GmaQL#OQXKCwFPxAnefvoxmiO5WF6kAlCe3QU76ivJocnNMFQ')
    title = models.CharField('title', max_length=50)
    description = models.TextField('description')
    count = models.IntegerField('count', default=0)

    def __str__(self):
        return 'Image - {0}, Title - {1}, Description - {2}'.format(self.image, self.title, self.description)


class Order(models.Model):
    id = models.AutoField('id', primary_key=True, auto_created=True)
    title = models.CharField('title', max_length=50)
    name_of_user = models.CharField('name_of_user', max_length=60)
    phone = models.CharField('phone', max_length=50)
    count = models.IntegerField('count')
    address = models.TextField('address')
    district = models.IntegerField('district')
    courier = models.TextField('courier', blank=True, null=True)
    status = models.IntegerField('status', default=0)

    def __str__(self):
        return 'Number - {0}, Title - {1}, Phone - {2}, Count - {3} Address - {4}, District - {5}, Courier - {6}'.format(self.id, self.title, self.phone, self.count, self.address, self.district, self.courier)


class Courier(models.Model):
    id = models.AutoField('id', primary_key=True, auto_created=True)
    name = models.CharField('name', max_length=50)
    nickname = models.CharField('nickname', max_length=50, blank=True)
    password = models.TextField('password', blank=True)
    district = models.IntegerField('district')
    invitation_code = models.CharField('invitation_code', max_length=11, default=key_gen)

    def __str__(self):
        return 'ID - {0} Name - {1}, District - {2}, Invitation Code - {3}'.format(self.id, self.name, self.district, self.invitation_code)
