# Generated by Django 4.0.3 on 2022-03-21 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_alter_items_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='desc',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
