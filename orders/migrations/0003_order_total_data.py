# Generated by Django 2.2.12 on 2022-09-13 09:55

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_vendors'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_data',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
    ]
