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
        return 'Name - {0}, Email - {1}, Invitation Code - {2}'.format(self.username, self.email, self.invitation_code)


class Product(models.Model):
    image = models.TextField('image', null=True, blank=True, default='https://mega.nz/file/389GmaQL#OQXKCwFPxAnefvoxmiO5WF6kAlCe3QU76ivJocnNMFQ')
    title = models.TextField('title')
    description = models.TextField('description')
    count = models.IntegerField('count', default=0)

    def __str__(self):
        return 'Image - {0}, Title - {1}, Description - {2}'.format(self.image, self.title, self.description)


class Order(models.Model):
    id = models.AutoField('id', primary_key=True, auto_created=True)
    title = models.TextField('title')
    name_of_user = models.TextField('name_of_user')
    phone = models.TextField('phone')
    count = models.IntegerField('count')
    address = models.TextField('address')
    district = models.IntegerField('district')
    courier = models.TextField('courier')

    def __str__(self):
        return 'Number - {0}, Title - {1}, Phone - {2}, Count - {3} Address - {4}, District - {5}, Courier - {6}'.format(self.id, self.title, self.phone, self.count, self.address, self.district, self.courier)


class Courier(models.Model):
    id = models.AutoField('id', primary_key=True, auto_created=True)
    name = models.TextField('name')
    district = models.IntegerField('district')

    def __str__(self):
        return 'Name - {0}, District - {1}'.format(self.name, self.district)
