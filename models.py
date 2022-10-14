# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Post(models.Model):
    profile_username = models.ForeignKey('Profile', models.DO_NOTHING, db_column='profile_username')
    textpost = models.TextField(blank=True, null=True)
    post_id = models.IntegerField(primary_key=True)
    

    class Meta:
        managed = False
        db_table = 'post'


class Profile(models.Model):
    username = models.TextField(primary_key=True)
    password = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profile'
