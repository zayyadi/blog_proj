# Generated by Django 3.1.4 on 2021-07-19 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210719_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.FilePathField(path='/Users/MIS-POLAR/Desktop/ourblog/ourblog/static/images'),
        ),
    ]
