# Generated by Django 3.2.8 on 2021-11-01 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_student', '0005_auto_20211027_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='scores',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
