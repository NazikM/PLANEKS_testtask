# Generated by Django 4.1.7 on 2023-03-13 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csv_generator', '0003_datasets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasets',
            name='csv_file',
            field=models.FileField(blank=True, default=None, null=True, upload_to='datasets/'),
        ),
    ]
