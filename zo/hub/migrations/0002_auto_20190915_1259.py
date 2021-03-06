# Generated by Django 2.2.4 on 2019-09-15 00:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hub',
            name='contact_details',
        ),
        migrations.AlterField(
            model_name='hub',
            name='main_contact',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='main_contact', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='hub',
            name='permission_admin',
            field=models.ManyToManyField(related_name='hub_permission_admin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='hub',
            name='permission_staff',
            field=models.ManyToManyField(related_name='hub_permission_staff', to=settings.AUTH_USER_MODEL),
        ),
    ]
