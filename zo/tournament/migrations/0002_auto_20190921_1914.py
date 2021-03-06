# Generated by Django 2.2.4 on 2019-09-21 07:14

from django.db import migrations, models
import django.db.models.deletion
import djangoyearlessdate.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_auto_20190917_1319'),
        ('tournament', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgeGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open', models.BooleanField(default=False)),
                ('under', models.BooleanField(default=True)),
                ('age', models.PositiveIntegerField(null=True)),
                ('yearless', djangoyearlessdate.models.YearlessDateField(max_length=4, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grade', to='tournament.AgeGrade')),
                ('gender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grade', to='user.Gender')),
            ],
        ),
        migrations.CreateModel(
            name='MeasurementType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RankGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, max_length=30)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ScoredByMeasurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('best_is_highest_value', models.BooleanField()),
                ('measurement_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.MeasurementType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='contesttypejumphorizontal',
            name='rules',
        ),
        migrations.RemoveField(
            model_name='contesttypejumpvertical',
            name='rules',
        ),
        migrations.RemoveField(
            model_name='contesttyperacerunning',
            name='rules',
        ),
        migrations.RemoveField(
            model_name='contesttyperaceswimming',
            name='rules',
        ),
        migrations.RemoveField(
            model_name='contesttypethrow',
            name='rules',
        ),
        migrations.AlterField(
            model_name='contest',
            name='content_type',
            field=models.ForeignKey(limit_choices_to={'pk__in': ()}, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.CreateModel(
            name='ScoredByMeasurementAttempts',
            fields=[
                ('scoredbymeasurement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tournament.ScoredByMeasurement')),
            ],
            options={
                'abstract': False,
            },
            bases=('tournament.scoredbymeasurement',),
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('rank_value', models.PositiveIntegerField(blank=True)),
                ('rank_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rank', to='tournament.RankGroup')),
            ],
        ),
        migrations.CreateModel(
            name='GradeName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='name', to='tournament.Grade')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade_name', to='tournament.Tournament')),
            ],
        ),
        migrations.AddField(
            model_name='grade',
            name='ranks',
            field=models.ManyToManyField(related_name='grade', to='tournament.Rank'),
        ),
        migrations.CreateModel(
            name='EventName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='name', to='tournament.Event')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_name', to='tournament.Tournament')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='contest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='tournament.Contest'),
        ),
        migrations.AddField(
            model_name='event',
            name='grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='tournament.Grade'),
        ),
        migrations.CreateModel(
            name='AgeGradeName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('age_grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='age_grade_name', to='tournament.AgeGrade')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='age_grade_name', to='tournament.Tournament')),
            ],
        ),
        migrations.AddField(
            model_name='contesttypejumphorizontal',
            name='scored_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tournament.ScoredByMeasurement'),
        ),
        migrations.AddField(
            model_name='contesttyperacerunning',
            name='scored_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tournament.ScoredByMeasurement'),
        ),
        migrations.AddField(
            model_name='contesttyperaceswimming',
            name='scored_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tournament.ScoredByMeasurement'),
        ),
        migrations.AddField(
            model_name='contesttypethrow',
            name='scored_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tournament.ScoredByMeasurement'),
        ),
        migrations.AddField(
            model_name='measurementunitgroup',
            name='measurement_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tournament.MeasurementType'),
        ),
        migrations.AddField(
            model_name='contesttypejumpvertical',
            name='scored_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tournament.ScoredByMeasurementAttempts'),
        ),
    ]
