import os

from django.conf import settings
from django.db import models

class React(models.Model):
    inputText = models.CharField(max_length=30)


class File(models.Model):
    file = models.FileField(upload_to='uploads/', blank=True, null=True) 