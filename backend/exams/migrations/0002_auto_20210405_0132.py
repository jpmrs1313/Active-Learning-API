# Generated by Django 3.1.7 on 2021-04-05 00:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exam',
            options={'ordering': ['id_exam']},
        ),
        migrations.RenameField(
            model_name='exam',
            old_name='ExamDate',
            new_name='exam_date',
        ),
        migrations.RenameField(
            model_name='exam',
            old_name='ExamNotes',
            new_name='exam_notes',
        ),
        migrations.RenameField(
            model_name='exam',
            old_name='ExamResult',
            new_name='exam_result',
        ),
        migrations.RenameField(
            model_name='exam',
            old_name='ExamType',
            new_name='exam_type',
        ),
        migrations.RenameField(
            model_name='exam',
            old_name='IDExam',
            new_name='id_exam',
        ),
    ]
