# Generated by Django 3.2.19 on 2023-12-21 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_parent',
            field=models.BooleanField(default=True),
        ),
    ]