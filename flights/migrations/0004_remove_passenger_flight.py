# Generated by Django 5.1.3 on 2024-12-13 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0003_passenger_flight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passenger',
            name='flight',
        ),
    ]
