# Generated by Django 4.1.7 on 2023-03-18 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_product_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='feedback',
            field=models.TextField(blank=True, null=True),
        ),
    ]
