# Generated by Django 3.2.19 on 2023-12-18 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_teacher_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='date_of_posted',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]