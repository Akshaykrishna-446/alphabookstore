# Generated by Django 5.1.1 on 2024-09-28 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alphabookapp', '0007_cart_book_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='cart',
        ),
    ]
