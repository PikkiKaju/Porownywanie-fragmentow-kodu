from django.db import models

class React(models.Model):
    inputText = models.CharField(max_length=30)