# Generated by Django 5.2 on 2025-04-16 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_rename_favouites_profile_favourites'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pass_reset_token',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
