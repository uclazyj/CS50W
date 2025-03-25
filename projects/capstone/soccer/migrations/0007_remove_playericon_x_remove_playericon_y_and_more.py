# Generated by Django 5.1.4 on 2025-03-25 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soccer', '0006_remove_image_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playericon',
            name='x',
        ),
        migrations.RemoveField(
            model_name='playericon',
            name='y',
        ),
        migrations.AddField(
            model_name='playericon',
            name='x_proportion',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='playericon',
            name='y_proportion',
            field=models.FloatField(null=True),
        ),
    ]
