# Generated by Django 4.0.5 on 2023-04-07 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_customer_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.FloatField(default=0, max_length=10),
        ),
    ]