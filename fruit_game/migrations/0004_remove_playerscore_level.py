# Generated by Django 5.1.1 on 2024-10-03 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fruit_game', '0003_alter_playerscore_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playerscore',
            name='level',
        ),
    ]
