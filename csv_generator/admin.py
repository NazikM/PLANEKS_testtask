from django.contrib import admin

from csv_generator.models import Schema, Datasets

admin.site.register(Schema)
admin.site.register(Datasets)
