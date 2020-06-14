# Generated by Django 3.0.2 on 2020-05-11 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_admin', '0034_auto_20200508_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='program_module',
            name='comments',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='questions',
            name='question_type',
            field=models.CharField(choices=[('Multiple Choice', 'Multiple Choice'), ('Fill Ups', 'Fill Ups'), ('Jumbled Words', 'Jumbled Words'), ('Riddles', 'Riddles')], max_length=100),
        ),
    ]