# Generated by Django 2.1.5 on 2019-02-07 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_username', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Username')),
                ('user_password', models.CharField(max_length=50, verbose_name='Password')),
                ('user_gender', models.CharField(choices=[('Female', 'Female'), ('Male', 'Male')], default='Male', max_length=10, verbose_name='Gender')),
                ('user_createTime', models.DateField(auto_now_add=True, verbose_name='CreatTime')),
                ('user_email', models.CharField(blank=True, max_length=20, null=True, verbose_name='Email')),
                ('user_province', models.CharField(blank=True, max_length=20, null=True, verbose_name='Province')),
                ('user_city', models.CharField(blank=True, max_length=20, null=True, verbose_name='City')),
                ('user_bio', models.CharField(blank=True, max_length=100, null=True, verbose_name='Bio')),
                ('user_favouritegame', models.CharField(blank=True, max_length=50, null=True, verbose_name='Favourite game')),
                ('user_cellphone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Cell phone')),
                ('user_image', models.ImageField(blank=True, null=True, upload_to='user')),
            ],
        ),
    ]
