# Generated by Django 4.2.15 on 2024-09-11 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0003_alter_menssagem_plataforma_msg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menssagem_plataforma',
            name='msg',
            field=models.CharField(max_length=250),
        ),
    ]