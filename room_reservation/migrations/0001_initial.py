# Generated by Django 3.0.6 on 2020-05-17 08:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccommodationModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accommodation_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('number_of_beds', models.IntegerField(choices=[('1', 'One'), ('2', 'Two'), ('3', 'Three'), ('4', 'Four'), ('5', 'Five'), ('6', 'Six')])),
                ('balcony', models.BooleanField()),
                ('price_per_night', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='HotelModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=255)),
                ('hotel_name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('hotel_image', models.ImageField(upload_to=None)),
            ],
        ),
        migrations.CreateModel(
            name='ReservationModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_date', models.DateField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('accommodation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room_reservation.AccommodationModel')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='accommodationmodel',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room_reservation.HotelModel'),
        ),
        migrations.CreateModel(
            name='AccommodationImageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to=None)),
                ('accommodation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room_reservation.AccommodationModel')),
            ],
        ),
    ]
