# Generated by Django 3.2.19 on 2024-02-19 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0003_assignment_teacher'),
        ('teacher', '0002_teacher_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='task_assign',
            field=models.ManyToManyField(blank=True, to='task_app.Task'),
        ),
    ]