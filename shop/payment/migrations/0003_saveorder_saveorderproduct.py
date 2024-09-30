# Generated by Django 4.2.16 on 2024-09-24 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_alter_shippingaddress_order_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaveOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('total_price', models.FloatField(default=0)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.customer')),
            ],
        ),
        migrations.CreateModel(
            name='SaveOrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=250)),
                ('quantity', models.IntegerField(default=0)),
                ('product_price', models.FloatField()),
                ('final_price', models.FloatField()),
                ('color', models.CharField(max_length=250)),
                ('size', models.CharField(max_length=250)),
                ('added_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='payment.saveorder')),
            ],
        ),
    ]
