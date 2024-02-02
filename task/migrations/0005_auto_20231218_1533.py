# Generated by Django 3.2.19 on 2023-12-18 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_student_user'),
        ('teacher', '0003_teacher_date_of_posted'),
        ('task', '0004_task_date_of_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assigned_student',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='student.Student'),
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned_teacher',
            field=models.ManyToManyField(blank=True, related_name='assigned_tasks', to='teacher.Teacher'),
        ),
    ]
