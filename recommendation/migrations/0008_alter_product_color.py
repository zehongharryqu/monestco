# Generated by Django 3.2.8 on 2022-02-08 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0007_remove_product_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
