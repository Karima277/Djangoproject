# Generated by Django 5.0 on 2023-12-28 22:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myfirstapp', '0002_promotion'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='promotion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myfirstapp.promotion'),
        ),
    ]
