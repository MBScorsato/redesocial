# Generated by Django 4.2.15 on 2024-10-16 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('galeria', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imgpublica',
            old_name='descicao',
            new_name='descricao',
        ),
    ]
