# Generated by Django 3.0.2 on 2021-06-01 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Face',
            new_name='Person',
        ),
        migrations.RenameField(
            model_name='photo',
            old_name='faces',
            new_name='people',
        ),
    ]