# Generated by Django 2.2.4 on 2019-09-01 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20190901_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(blank=True, max_length=50, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='address',
            name='line1',
            field=models.CharField(max_length=50, verbose_name='Address Line 1'),
        ),
        migrations.AlterField(
            model_name='address',
            name='line2',
            field=models.CharField(blank=True, max_length=50, verbose_name='Address Line 2'),
        ),
        migrations.AlterField(
            model_name='address',
            name='line3',
            field=models.CharField(blank=True, max_length=50, verbose_name='Address Line 3'),
        ),
        migrations.AlterField(
            model_name='address',
            name='postcode',
            field=models.CharField(blank=True, max_length=50, verbose_name='Postcode'),
        ),
        migrations.AlterField(
            model_name='address',
            name='town_city',
            field=models.CharField(max_length=50, verbose_name='Town/City'),
        ),
    ]