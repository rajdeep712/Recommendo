# Generated by Django 5.2 on 2025-04-13 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_comment_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='vote_count',
            field=models.IntegerField(null=True),
        ),
    ]
