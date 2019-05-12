# Generated by Django 2.1.5 on 2019-05-12 16:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookDetails', '0013_auto_20190412_1835'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='name',
            new_name='display_name',
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=3, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)]),
        ),
    ]