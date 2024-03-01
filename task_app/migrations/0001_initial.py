# Generated by Django 3.2.19 on 2024-03-01 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgeGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age_group', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assessment_file', models.FileField(blank=True, null=True, upload_to='user_image')),
                ('is_completed', models.BooleanField(default=False)),
                ('completion_date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_type', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='user_image')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField()),
                ('submission_date', models.CharField(blank=True, max_length=200, null=True)),
                ('is_completed', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('expired', 'Expired')], default='pending', max_length=200)),
                ('date_of_posted', models.DateField(auto_now_add=True, null=True)),
                ('age_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='task_app.agegroup')),
                ('assigned_student', models.ManyToManyField(blank=True, related_name='tasks', to='student.Student')),
            ],
        ),
    ]
