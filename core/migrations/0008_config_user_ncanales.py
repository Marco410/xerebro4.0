# Generated by Django 2.2.3 on 2020-07-11 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_config_user_file_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='config_user',
            name='ncanales',
            field=models.IntegerField(null=True),
        ),
    ]
