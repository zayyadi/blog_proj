# Generated by Django 3.1.4 on 2021-07-23 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210723_0921'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='name',
            new_name='author',
        ),
    ]