# Generated by Django 4.1.5 on 2023-02-24 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kpmbParking', '0004_parking'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('bookingID', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('bookingDate', models.DateField()),
                ('bookingTime', models.TimeField()),
                ('remark', models.TextField()),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('parkingID', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='kpmbParking.parking')),
                ('studentID', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='kpmbParking.student')),
            ],
        ),
    ]