# Generated by Django 5.1.4 on 2025-03-09 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soccer', '0002_playericon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playericon',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
