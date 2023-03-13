from django.contrib.auth.models import User
from django.db import models


class Schema(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    separator = models.CharField(max_length=1)
    string_char = models.CharField(max_length=2)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    columns = models.JSONField()

    def __str__(self):
        return self.name


class Datasets(models.Model):
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    status_choices = [
        ('P', 'Processing'),
        ('R', 'Ready'),
    ]
    csv_file = models.FileField(upload_to='datasets/', null=True, blank=True, default=None)
    status = models.CharField(max_length=1, choices=status_choices)
    date_created = models.DateField(auto_now_add=True)
