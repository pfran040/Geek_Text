# Generated by Django 2.1.5 on 2019-04-12 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookDetails', '0006_auto_20190412_0143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='avg_rating',
            field=models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=2, null=True),
        ),
    ]
