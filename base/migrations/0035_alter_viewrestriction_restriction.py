# Generated by Django 3.2.20 on 2024-01-26 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0034_alter_viewrestriction_restriction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewrestriction',
            name='restriction',
            field=models.CharField(choices=[('PU', 'Public'), ('ST', 'Student Only'), ('PV', 'Private')], default='PU', max_length=150),
        ),
    ]
