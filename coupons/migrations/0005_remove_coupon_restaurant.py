# Generated by Django 3.2 on 2021-06-14 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0004_couponused'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='restaurant',
        ),
    ]
