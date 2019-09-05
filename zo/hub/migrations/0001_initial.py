# Generated by Django 2.2.4 on 2019-09-04 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0007_auto_20190904_2235'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hub',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('School', 'School'), ('Sports Club', 'Sports Club'), ('Other', 'Other')], max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('is_public', models.BooleanField(default=False)),
                ('contact_details', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.ContactDetails')),
                ('main_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_contact', to=settings.AUTH_USER_MODEL)),
                ('permission_admin', models.ManyToManyField(related_name='permission_admin', to=settings.AUTH_USER_MODEL)),
                ('permission_staff', models.ManyToManyField(related_name='permission_staff', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
