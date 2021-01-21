# Generated by Django 2.2.13 on 2021-01-19 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_admin', '0002_assessment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='assessment_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user_admin.assessment_type'),
        ),
        migrations.AlterField(
            model_name='assessment_type',
            name='assessment_type',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
