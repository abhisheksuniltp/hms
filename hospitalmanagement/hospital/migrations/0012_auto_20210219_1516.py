# Generated by Django 3.1.5 on 2021-02-19 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0011_auto_20210219_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='department',
            field=models.CharField(choices=[('General Physician', 'General Physician'), ('Pediatrician', 'Pediatrician'), ('General Surgeon', 'General Surgeon'), ('Dentist', 'Dentist'), ('ENT Specialist', 'ENT Specialist'), ('Cardiologist', 'Cardiologist'), ('Dermatologists', 'Dermatologists'), ('Emergency Medicine Specialists', 'Emergency Medicine Specialists'), ('Allergists/Immunologists', 'Allergists/Immunologists'), ('Anesthesiologists', 'Anesthesiologists'), ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons')], default='Cardiologist', max_length=128),
        ),
    ]
