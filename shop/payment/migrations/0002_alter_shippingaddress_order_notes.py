# Generated by Django 4.2.16 on 2024-09-22 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='order_notes',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
