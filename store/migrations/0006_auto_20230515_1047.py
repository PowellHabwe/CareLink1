# Generated by Django 3.1.1 on 2023-05-15 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20230515_1043'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hospital',
            old_name='availabile_services',
            new_name='availabile_services_and_resource',
        ),
    ]
