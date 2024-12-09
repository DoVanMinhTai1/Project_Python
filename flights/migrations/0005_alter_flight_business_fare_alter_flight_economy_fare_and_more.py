# Generated by Django 5.0.10 on 2024-12-08 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0004_alter_flight_business_fare_alter_flight_economy_fare_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='business_fare',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='flight',
            name='economy_fare',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True),
        ),
        migrations.AlterField(
            model_name='flight',
            name='first_fare',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True),
        ),
    ]