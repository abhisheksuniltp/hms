# Generated by Django 3.1.5 on 2021-02-17 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='amountReceived',
        ),
    ]
