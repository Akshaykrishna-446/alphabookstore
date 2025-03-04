# Generated by Django 5.1.1 on 2024-09-28 19:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alphabookapp', '0008_delete_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('book_id', models.IntegerField(primary_key=True, serialize=False)),
                ('book_cover', models.CharField(max_length=200, null=True)),
                ('book_title', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order_qty', models.IntegerField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='added_items', to='alphabookapp.user_register')),
            ],
        ),
    ]
