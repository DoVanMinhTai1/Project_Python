# Generated by Django 5.1.3 on 2024-12-07 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_remove_booking_abc_booking_flight_id_and_more'),
        ('flights', '0002_place_week_remove_flights_price_per_seat_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Flights',
            new_name='Flight',
        ),
    ]