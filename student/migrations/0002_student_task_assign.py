# Generated by Django 3.2.19 on 2024-03-01 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
        ('task_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='task_assign',
            field=models.ManyToManyField(blank=True, to='task_app.Task'),
        ),
    ]