# Generated by Django 3.1.1 on 2023-05-15 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20230515_0743'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicalstaff',
            old_name='hospital',
            new_name='hospital_name',
        ),
    ]
