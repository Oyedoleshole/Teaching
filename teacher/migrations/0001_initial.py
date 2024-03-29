# Generated by Django 3.2.19 on 2024-03-01 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0002_student_task_assign'),
        ('task_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='user_image')),
                ('date_of_posted', models.DateTimeField(auto_now_add=True, null=True)),
                ('date_and_time_of_task_assigned', models.CharField(blank=True, max_length=200, null=True)),
                ('students', models.ManyToManyField(blank=True, related_name='teachers', to='student.Student')),
                ('task_assign', models.ManyToManyField(blank=True, to='task_app.Task')),
            ],
        ),
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
