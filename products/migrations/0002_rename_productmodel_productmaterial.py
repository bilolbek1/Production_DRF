# Generated by Django 5.0.3 on 2024-03-14 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductModel',
            new_name='ProductMaterial',
        ),
    ]
