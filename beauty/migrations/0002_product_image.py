# Generated by Django 4.2.21 on 2025-05-11 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beauty', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/'),
        ),
    ]
