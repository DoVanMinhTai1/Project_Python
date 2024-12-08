# Generated by Django 5.1.3 on 2024-12-07 08:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='flights',
            name='price_per_seat',
        ),
        migrations.RemoveField(
            model_name='flights',
            name='source',
        ),
        migrations.AddField(
            model_name='flights',
            name='business_fare',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True),
        ),
        migrations.AddField(
            model_name='flights',
            name='economy_fare',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True),
        ),
        migrations.AddField(
            model_name='flights',
            name='first_fare',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True),
        ),
        migrations.AddField(
            model_name='flights',
            name='origin',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='departure_flights', to='flights.place'),
        ),
        migrations.AlterField(
            model_name='flights',
            name='destination',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arrival_flights', to='flights.place'),
        ),
        migrations.AddField(
            model_name='flights',
            name='depart_day',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flights', to='flights.week'),
        ),
    ]
