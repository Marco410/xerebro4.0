# Generated by Django 2.2.3 on 2020-06-25 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200624_0958'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='config_user',
            options={'ordering': ['created_at']},
        ),
        migrations.AddField(
            model_name='config_user',
            name='active',
            field=models.TextField(null=True),
        ),
    ]
