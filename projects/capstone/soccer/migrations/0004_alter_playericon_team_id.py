# Generated by Django 5.1.4 on 2025-03-13 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soccer', '0003_alter_playericon_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playericon',
            name='team_id',
            field=models.IntegerField(default=0),
        ),
    ]
