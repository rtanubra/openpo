# Generated by Django 3.0.7 on 2020-06-23 00:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20200623_0022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='seller',
        ),
    ]
