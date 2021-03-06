# Generated by Django 2.2.4 on 2019-10-09 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0011_auto_20190926_1323'),
    ]

    operations = [
        migrations.CreateModel(
            name='RankGroupType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
            ],
        ),
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
            model_name='rank',
            name='rank_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ranks', to='tournament.RankGroup'),
        ),
        migrations.AlterField(
            model_name='rankgroup',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rank_groups', to='tournament.RankGroupType'),
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
