# Generated by Django 3.2 on 2021-04-20 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('als', '0004_al_activated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='al',
            name='activated',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
