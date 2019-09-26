# Generated by Django 2.2.4 on 2019-09-26 01:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0010_auto_20190925_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='content_type',
            field=models.ForeignKey(limit_choices_to={'pk__in': ()}, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='contestinstance',
            name='content_type',
            field=models.ForeignKey(limit_choices_to={'pk__in': ()}, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='roundsystem',
            name='content_type',
            field=models.ForeignKey(limit_choices_to={'pk__in': ()}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='score',
            name='content_type',
            field=models.ForeignKey(limit_choices_to={'pk__in': ()}, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]
