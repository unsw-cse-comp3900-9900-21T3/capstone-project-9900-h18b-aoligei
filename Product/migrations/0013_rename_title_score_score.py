# Generated by Django 3.2.7 on 2021-10-28 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0012_score'),
    ]

    operations = [
        migrations.RenameField(
            model_name='score',
            old_name='title',
            new_name='score',
        ),
    ]