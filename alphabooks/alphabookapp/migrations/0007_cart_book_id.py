# Generated by Django 5.1.1 on 2024-09-28 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alphabookapp', '0006_remove_order_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='book_id',
            field=models.IntegerField(null=True),
        ),
    ]
