# Generated by Django 3.2.20 on 2024-01-29 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0037_alter_viewrestriction_restriction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewrestriction',
            name='restriction',
            field=models.CharField(choices=[('Private', 'Private'), ('Student Only', 'Student Only'), ('Public', 'Public')], default='Public', max_length=150),
        ),
    ]
