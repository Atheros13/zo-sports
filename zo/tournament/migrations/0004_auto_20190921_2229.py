# Generated by Django 2.2.4 on 2019-09-21 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hub', '0005_auto_20190921_1914'),
        ('tournament', '0003_auto_20190921_1918'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('sub_activities', models.ManyToManyField(related_name='_activity_sub_activities_+', to='tournament.Activity')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TournamentEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tournament_events', to='tournament.Event')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentStone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='tournamentcompetitorgroup',
            name='competitor_group',
        ),
        migrations.RemoveField(
            model_name='tournamentcompetitorgroup',
            name='tournament',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='competitor',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='master',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='name',
        ),
        migrations.AddField(
            model_name='competitor',
            name='participant',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competitor', to='tournament.Participant'),
        ),
        migrations.AddField(
            model_name='competitor',
            name='tournament',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competitors', to='tournament.Tournament'),
        ),
        migrations.AddField(
            model_name='participant',
            name='tournament',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='tournament.Tournament'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='competitor_groups',
            field=models.ManyToManyField(related_name='tournaments', to='tournament.CompetitorGroup'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='contests',
            field=models.ManyToManyField(related_name='tournaments', to='tournament.Contest'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tournaments_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tournament',
            name='created_on',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='tournament',
            name='grades',
            field=models.ManyToManyField(related_name='tournaments', to='tournament.Grade'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='hubs',
            field=models.ManyToManyField(related_name='tournaments', to='hub.Hub'),
        ),
        migrations.AlterField(
            model_name='competitor',
            name='competitor_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='competitors', to='tournament.CompetitorGroup'),
        ),
        migrations.AlterField(
            model_name='contest',
            name='content_type',
            field=models.ForeignKey(limit_choices_to={'pk__in': ()}, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='gradename',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade_names', to='tournament.Tournament'),
        ),
        migrations.DeleteModel(
            name='EventName',
        ),
        migrations.DeleteModel(
            name='TournamentCompetitorGroup',
        ),
        migrations.DeleteModel(
            name='TournamentMaster',
        ),
        migrations.AddField(
            model_name='tournamentname',
            name='tournament',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='name', to='tournament.Tournament'),
        ),
        migrations.AddField(
            model_name='tournamentevent',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='tournament.Tournament'),
        ),
        migrations.AddField(
            model_name='activity',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='tournament.ActivityType'),
        ),
        migrations.AddField(
            model_name='contest',
            name='activity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contests', to='tournament.Activity'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='activity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tournaments', to='tournament.Activity'),
        ),
    ]
