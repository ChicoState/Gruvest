# Generated by Django 3.1.1 on 2020-12-09 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StocksModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10)),
                ('date', models.DateField()),
                ('closingPrice', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('percentageChange', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
            ],
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=100)),
                ('post', models.CharField(max_length=5000)),
                ('upVotes', models.IntegerField(default=0)),
                ('downVotes', models.IntegerField(default=0)),
                ('cost', models.PositiveIntegerField(default=1)),
                ('published_on', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UpvoteModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upvotedPost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upvoted_post', to='myapp.usermodel')),
                ('upvoter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upvote_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TrackedStocksModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='', max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
                ('category', models.CharField(choices=[(0, 'BUY'), (1, 'HOLD'), (2, 'SELL')], default=1, max_length=4)),
                ('data', models.ManyToManyField(to='myapp.StocksModel')),
                ('pitcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='SubscribeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pitcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pitcher_user', to=settings.AUTH_USER_MODEL)),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcribe_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchasedPost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchased_post', to='myapp.usermodel')),
                ('purchaser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DownvoteModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('downvotedPost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='downvoted_post', to='myapp.usermodel')),
                ('downvoter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='downvote_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=240)),
                ('published_on', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='myapp.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='CatcherModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('funds', models.PositiveIntegerField(default=0, verbose_name='Add amount')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
