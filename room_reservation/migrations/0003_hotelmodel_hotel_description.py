# Generated by Django 3.0.6 on 2020-05-17 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_reservation', '0002_auto_20200517_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelmodel',
            name='hotel_description',
            field=models.TextField(default=''),
        ),
    ]