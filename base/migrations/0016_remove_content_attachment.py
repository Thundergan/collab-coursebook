# Generated by Django 3.0.7 on 2021-02-26 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_auto_20210222_1306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='attachment',
        ),
    ]
