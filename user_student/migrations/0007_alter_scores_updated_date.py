# Generated by Django 3.2.8 on 2021-11-09 09:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user_student', '0006_scores_updated_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scores',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
