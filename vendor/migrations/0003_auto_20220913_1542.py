# Generated by Django 2.2.12 on 2022-09-13 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_vendor_shop_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendor',
            old_name='shop_slug',
            new_name='slug',
        ),
    ]