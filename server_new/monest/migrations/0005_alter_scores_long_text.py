# Generated by Django 3.2.8 on 2021-11-13 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monest', '0004_alter_scores_long_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scores',
            name='long_text',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]
