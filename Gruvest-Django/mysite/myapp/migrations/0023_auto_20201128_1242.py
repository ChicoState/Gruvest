# Generated by Django 3.1.2 on 2020-11-28 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0022_remove_stocksmodel_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocksmodel',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='trackedstocksmodel',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
