# Generated by Django 3.1.1 on 2023-05-16 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20230516_2029'),
    ]

    operations = [
        migrations.CreateModel(
            name='HospitalService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pricing', models.CharField(max_length=200)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hospital_services', to='store.hospital')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.service')),
            ],
        ),
    ]
