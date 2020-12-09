# Generated by Django 3.1.2 on 2020-11-27 22:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_auto_20201126_0832'),
    ]

    operations = [
        migrations.CreateModel(
            name='StocksModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ticker', models.CharField(max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('closingPrice', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('percentageChange', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
            ],
        ),
        migrations.RemoveField(
            model_name='trackedstocksmodel',
            name='accuracy',
        ),
        migrations.AddField(
            model_name='trackedstocksmodel',
            name='description',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.RemoveField(
            model_name='trackedstocksmodel',
            name='data',
        ),
        migrations.AlterField(
            model_name='trackedstocksmodel',
            name='pitcher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.usermodel'),
        ),
        migrations.AddField(
            model_name='trackedstocksmodel',
            name='data',
            field=models.ManyToManyField(to='myapp.StocksModel'),
        ),
    ]