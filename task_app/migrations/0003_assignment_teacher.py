# Generated by Django 3.2.19 on 2024-02-14 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_teacher_user'),
        ('task_app', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teacher.teacher'),
        ),
    ]