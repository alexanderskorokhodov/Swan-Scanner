from django.db import models

class React(models.Model):
    name = models.CharField(max_length=30000000000000000)
    detail = models.CharField(max_length=500)
# Create your models here.

class SendImage(models.Model):
    src = models.CharField(max_length = 100000000000000)
    image_id = models.CharField(max_length = 100000000000000)

class Image(models.Model):
    image_id = models.CharField(max_length = 100000000000)

class Note(models.Model):
    image_id = models.CharField(max_length = 100000000000)
    note = models.CharField(max_length = 100000000000)

class UploadImage(models.Model):
    image_id = models.CharField(max_length=290000000000000)
    image = models.ImageField(upload_to='images')