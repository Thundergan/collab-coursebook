# Generated by Django 3.2.20 on 2024-01-19 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_auto_20240119_1929'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='viewrestriction',
            options={'verbose_name': 'View Restriction'},
        ),
        migrations.AlterField(
            model_name='viewrestriction',
            name='restriction',
            field=models.CharField(choices=[('ST', 'Student Only'), ('PU', 'Public'), ('PV', 'Private')], default='PU', max_length=150),
        ),
    ]
