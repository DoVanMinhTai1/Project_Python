# Generated by Django 5.1.3 on 2025-01-08 08:29

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('flights', '0015_remove_ticket_passengers_remove_ticket_flight_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=120, null=True)),
                ('last_name', models.CharField(max_length=120, null=True)),
                ('gender', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fare', models.DecimalField(decimal_places=2, max_digits=18)),
                ('card_number', models.CharField(max_length=20, null=True)),
                ('card_holder_name', models.CharField(max_length=150, null=True)),
                ('expMonth', models.IntegerField(null=True)),
                ('expYear', models.IntegerField(null=True)),
                ('cvv', models.IntegerField(null=True)),
                ('status', models.CharField(default='paid', max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_name', models.CharField(max_length=20)),
                ('price', models.FloatField()),
                ('type', models.CharField(choices=[('economy', 'Economy'), ('business', 'Business'), ('first', 'First')], max_length=20)),
                ('status', models.CharField(choices=[('AVAILABLE', 'Available'), ('SELECTED', 'Selected')], max_length=20)),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flights.flight')),
            ],
            options={
                'db_table': 'payment_seat',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_no', models.CharField(max_length=6, unique=True)),
                ('flight_ddate', models.DateField(blank=True, null=True)),
                ('flight_adate', models.DateField(blank=True, null=True)),
                ('flight_fare', models.FloatField(blank=True, null=True)),
                ('other_charges', models.FloatField(blank=True, null=True)),
                ('coupon_used', models.CharField(blank=True, max_length=15)),
                ('coupon_discount', models.FloatField(default=0.0)),
                ('total_fare', models.FloatField(blank=True, null=True)),
                ('seat_class', models.CharField(choices=[('economy', 'Economy'), ('business', 'Business'), ('first', 'First')], max_length=20)),
                ('booking_date', models.DateTimeField(default=datetime.datetime.now)),
                ('mobile', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=45)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('CONFIRMED', 'Confirmed'), ('CANCELLED', 'Cancelled')], max_length=45)),
                ('flight', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='flights.flight')),
                ('passengers', models.ManyToManyField(related_name='flight_tickets', to='payment.passenger')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.payment')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.ticket')),
            ],
        ),
        migrations.CreateModel(
            name='TicketSeat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.seat')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.ticket')),
            ],
        ),
    ]
