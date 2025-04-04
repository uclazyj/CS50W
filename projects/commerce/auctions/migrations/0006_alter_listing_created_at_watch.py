# Generated by Django 5.1.4 on 2025-01-27 15:21

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_created_at_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.localtime),
        ),
        migrations.CreateModel(
            name='Watch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
