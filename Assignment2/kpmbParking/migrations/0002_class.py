# Generated by Django 4.1.5 on 2023-02-24 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpmbParking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('classID', models.CharField(max_length=5, primary_key=True, serialize=False)),
            ],
        ),
    ]
