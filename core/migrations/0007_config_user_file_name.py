# Generated by Django 2.2.3 on 2020-07-10 03:38

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_tablesuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='config_user',
            name='file_name',
            field=models.FileField(blank=True, null=True, upload_to=core.models.custom_upload_to),
        ),
    ]
