# Generated by Django 3.2.19 on 2024-02-08 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0003_alter_task_is_completed'),
        ('teacher', '0002_teacher_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeacherAddRemarkandImageForExistinceTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_image_for_hint', models.FileField(blank=True, null=True, upload_to='user_image')),
                ('remark', models.TextField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='task_app.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.teacher')),
            ],
        ),
    ]
