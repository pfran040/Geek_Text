# Generated by Django 2.1.5 on 2019-02-16 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20190216_0324'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name_plural': 'Address'},
        ),
        migrations.AlterModelOptions(
            name='addressinfo',
            options={'verbose_name': 'Addresses of all users', 'verbose_name_plural': 'AddressInfo'},
        ),
    ]
