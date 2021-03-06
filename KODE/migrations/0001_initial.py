# Generated by Django 3.1.2 on 2020-10-28 13:41

import KODE.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('nickname', models.CharField(blank=True, max_length=50, verbose_name='nickname')),
                ('password', models.TextField(blank=True, verbose_name='password')),
                ('district', models.IntegerField(verbose_name='district')),
                ('invitation_code', models.CharField(default=KODE.models.key_gen, max_length=11, verbose_name='invitation_code')),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='username')),
                ('nickname', models.CharField(blank=True, max_length=50, verbose_name='nickname')),
                ('email', models.CharField(blank=True, max_length=100, verbose_name='email')),
                ('password', models.TextField(blank=True, verbose_name='password')),
                ('invitation_code', models.CharField(default=KODE.models.key_gen, max_length=11, verbose_name='invitation_code')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('name_of_user', models.CharField(max_length=50, verbose_name='name_of_user')),
                ('phone', models.CharField(max_length=50, verbose_name='phone')),
                ('count', models.IntegerField(verbose_name='count')),
                ('address', models.TextField(verbose_name='address')),
                ('district', models.IntegerField(verbose_name='district')),
                ('courier', models.IntegerField(blank=True, verbose_name='courier')),
                ('status', models.IntegerField(default=0, verbose_name='status')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.TextField(blank=True, default='https://mega.nz/file/389GmaQL#OQXKCwFPxAnefvoxmiO5WF6kAlCe3QU76ivJocnNMFQ', null=True, verbose_name='image')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('count', models.IntegerField(default=0, verbose_name='count')),
            ],
        ),
    ]
