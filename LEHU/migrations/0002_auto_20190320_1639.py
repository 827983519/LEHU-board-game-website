# Generated by Django 2.1.7 on 2019-03-20 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LEHU', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='Popular_board_game',
        ),
        migrations.AddField(
            model_name='store',
            name='Popular_board_game1',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='Popular_board_game2',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='Popular_board_game3',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
