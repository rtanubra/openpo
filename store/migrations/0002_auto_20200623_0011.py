# Generated by Django 3.0.7 on 2020-06-23 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='note',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='basket',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out for deliver', 'Out for delivery'), ('Delivered', 'Delivered')], max_length=200, null=True),
        ),
    ]
