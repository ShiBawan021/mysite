# Generated by Django 4.0.2 on 2022-03-08 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comenet_time',
            new_name='comment_time',
        ),
    ]
