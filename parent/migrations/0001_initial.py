# Generated by Django 3.2.19 on 2024-03-01 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='user_image')),
                ('date_of_posted', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
