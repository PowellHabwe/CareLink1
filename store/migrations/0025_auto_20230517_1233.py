# Generated by Django 3.1.1 on 2023-05-17 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_vehicle_price_per_km'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_type',
            field=models.CharField(choices=[('ambulance', 'Ambulance'), ('personal', 'Medical Shuttle')], max_length=20),
        ),
    ]
