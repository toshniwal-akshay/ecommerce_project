# Generated by Django 2.2.12 on 2022-09-13 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='vendors',
            field=models.ManyToManyField(blank=True, to='vendor.Vendor'),
        ),
    ]
