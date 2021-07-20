# Generated by Django 3.1.7 on 2021-03-26 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='pacients',
            fields=[
                ('IDPacient', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('IDPacientAnonym', models.IntegerField(unique=True)),
                ('FirstName', models.CharField(max_length=50)),
                ('LastName', models.CharField(max_length=50)),
                ('BirthDate', models.DateField()),
                ('Gender', models.CharField(max_length=50)),
                ('TotalExams', models.IntegerField(unique=True)),
                ('Remarks', models.TextField(max_length=1000)),
            ],
            options={
                'ordering': ['IDPacient'],
            },
        ),
    ]