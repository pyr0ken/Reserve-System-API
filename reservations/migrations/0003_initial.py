# Generated by Django 4.2.2 on 2023-06-16 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reservations', '0002_delete_reservations'),
    ]

    operations = [
        migrations.CreateModel(
            name='SonsTimes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('holiday_price', models.DecimalField(decimal_places=0, max_digits=10)),
            ],
        ),
    ]