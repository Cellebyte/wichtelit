# Generated by Django 3.1.2 on 2020-12-02 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wichtelit', '0008_auto_20200505_1648'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wichtelgruppe',
            old_name='ablaufdatum',
            new_name='anmeldeschluss',
        ),
    ]