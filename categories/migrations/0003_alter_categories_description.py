# Generated by Django 4.0.3 on 2022-03-21 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_alter_categories_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
