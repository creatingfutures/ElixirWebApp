# Generated by Django 2.2.13 on 2021-02-03 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scores',
            name='question_content_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]