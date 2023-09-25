# Generated by Django 3.1.5 on 2021-02-18 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0005_auto_20210218_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testName', models.CharField(blank=True, max_length=128, null=True)),
                ('testPrice', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='labresult',
            name='testId',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='labresult',
            name='testName',
            field=models.CharField(max_length=128),
        ),
    ]
