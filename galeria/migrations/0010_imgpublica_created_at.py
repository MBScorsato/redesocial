# Generated by Django 4.2.15 on 2024-10-16 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galeria', '0009_remove_imgpublica_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='imgpublica',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=11111),
            preserve_default=False,
        ),
    ]