from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class MyShelf(models.Model):
    user = models.ForeignKey(User)
    totalShelfLen = models.FloatField(null=True, blank=True, verbose_name='Bookshelf total length')
    lat = models.FloatField(null=True, blank=True, verbose_name='latitude')
    lng = models.FloatField(null=True, blank=True, verbose_name='longitude')


class MyBooks(models.Model):
    shelf = models.ForeignKey(MyShelf)
    bookTitle = models.TextField(max_length=600, null=True, blank=True)
    bookImgUri = models.TextField(null=True, blank=True, max_length=800)
    bookPublisher = models.TextField(null=True, blank=True,max_length=300)
    bookDesc = models.TextField(null=True, blank=True)
    bookInfo = models.TextField(verbose_name='Book information')
    booksPosLen = models.FloatField(null=True, blank=True, verbose_name='Book position')
    readPos = models.IntegerField(null=True, blank=True)
    remark = models.TextField()


class FcmToken(models.Model):
    tokenTypeChoices = (
        (0, 'Camera Application'),
        (1, 'User Application'),
    )
    shelf = models.ForeignKey(MyShelf)
    tokenType = models.IntegerField(choices=tokenTypeChoices)
    token = models.TextField(null=True, blank=True, max_length=600)
    remark = models.TextField(null=True, blank=True)
