# Generated by Django 3.2 on 2021-04-26 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('als', '0010_alter_al_model_weights'),
    ]

    operations = [
        migrations.AlterField(
            model_name='al',
            name='model_weights',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
