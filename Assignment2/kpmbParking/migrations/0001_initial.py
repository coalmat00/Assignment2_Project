# Generated by Django 4.1.5 on 2023-02-24 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('courseID', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('courseName', models.TextField()),
                ('courseDescription', models.TextField()),
            ],
        ),
    ]
