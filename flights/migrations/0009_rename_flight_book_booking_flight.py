# Generated by Django 5.1.3 on 2024-12-13 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0008_remove_passenger_flight_booking_flight_book_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='flight_book',
            new_name='flight',
        ),
    ]
