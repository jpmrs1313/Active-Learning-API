# Generated by Django 3.2 on 2021-04-25 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unlabeled', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='unlabeledimage',
            name='blocked',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
