# Generated by Django 4.2.15 on 2024-08-30 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagemIndex2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title2', models.CharField(max_length=100)),
                ('img2', models.ImageField(upload_to='img_index')),
            ],
        ),
    ]
