# Generated by Django 2.2.12 on 2022-09-13 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_auto_20220913_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
