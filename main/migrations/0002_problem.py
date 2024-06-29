# Generated by Django 4.2.13 on 2024-06-29 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
                ('problem_name', models.CharField(max_length=255)),
                ('problem_link', models.URLField(max_length=500)),
                ('difficulty', models.CharField(max_length=50)),
                ('topic', models.CharField(max_length=100)),
                ('subtopic', models.CharField(max_length=100)),
                ('final_youtube_link', models.URLField(blank=True, max_length=500, null=True)),
                ('record_by', models.CharField(max_length=100)),
                ('deadline', models.DateField()),
                ('small_hint', models.TextField(blank=True, null=True)),
                ('big_hint', models.TextField(blank=True, null=True)),
                ('reviewer_deadline', models.DateField()),
                ('remark_for_small_hint', models.TextField(blank=True, null=True)),
                ('remark_for_big_hint', models.TextField(blank=True, null=True)),
                ('hint_writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hint_written_problems', to='main.assigned_role')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewed_problems', to='main.assigned_role')),
            ],
        ),
    ]
