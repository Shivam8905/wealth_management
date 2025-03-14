# Generated by Django 4.2.20 on 2025-03-09 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=120)),
                ('date', models.DateField()),
                ('trade_type', models.PositiveSmallIntegerField(choices=[(1, 'Buy'), (2, 'Sell'), (3, 'Split')])),
                ('quantity', models.IntegerField()),
                ('price_per_share', models.DecimalField(decimal_places=3, max_digits=11)),
                ('split_ratio', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('company', models.CharField(max_length=120)),
                ('quantity', models.IntegerField()),
                ('price_per_share', models.DecimalField(decimal_places=3, max_digits=11)),
            ],
        ),
    ]
