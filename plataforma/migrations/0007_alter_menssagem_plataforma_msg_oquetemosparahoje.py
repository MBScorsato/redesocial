# Generated by Django 4.2.15 on 2024-09-13 12:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plataforma', '0006_alter_menssagem_plataforma_msg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menssagem_plataforma',
            name='msg',
            field=models.CharField(max_length=105),
        ),
        migrations.CreateModel(
            name='OQueTemosParaHoje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_hoje', models.CharField(max_length=105)),
                ('data', models.DateField(auto_now_add=True)),
                ('contador', models.IntegerField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]