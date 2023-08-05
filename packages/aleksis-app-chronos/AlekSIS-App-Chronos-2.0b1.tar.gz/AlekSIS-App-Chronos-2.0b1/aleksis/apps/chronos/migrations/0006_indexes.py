# Generated by Django 3.2 on 2021-04-08 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_external_link_widget'),
        ('chronos', '0005_add_permissions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chronosglobalpermissions',
            options={'managed': False, 'permissions': (('view_all_timetables', 'Can view all timetables'), ('view_timetable_overview', 'Can view timetable overview'), ('view_lessons_day', 'Can view all lessons per day'))},
        ),
        migrations.AlterModelOptions(
            name='lessonsubstitution',
            options={'ordering': ['year', 'week', 'lesson_period__period__weekday', 'lesson_period__period__period'], 'verbose_name': 'Lesson substitution', 'verbose_name_plural': 'Lesson substitutions'},
        ),
        migrations.RemoveIndex(
            model_name='event',
            name='chronos_eve_period__c7ec33_idx',
        ),
        migrations.RemoveIndex(
            model_name='lessonperiod',
            name='chronos_les_lesson__05250e_idx',
        ),
        migrations.AddIndex(
            model_name='event',
            index=models.Index(fields=['date_start', 'date_end'], include=('period_from', 'period_to'), name='event_date_start_date_end'),
        ),
        migrations.AddIndex(
            model_name='extralesson',
            index=models.Index(fields=['week', 'year'], name='extra_lesson_week_year'),
        ),
        migrations.AddIndex(
            model_name='lessonperiod',
            index=models.Index(fields=['lesson', 'period'], name='lesson_period_lesson_period'),
        ),
        migrations.AddIndex(
            model_name='lessonperiod',
            index=models.Index(fields=['room'], include=('lesson', 'period'), name='lesson_period_room'),
        ),
        migrations.AddIndex(
            model_name='lessonsubstitution',
            index=models.Index(fields=['week', 'year'], name='substitution_week_year'),
        ),
        migrations.AddIndex(
            model_name='lessonsubstitution',
            index=models.Index(fields=['lesson_period'], name='substitution_lesson_period'),
        ),
        migrations.AddIndex(
            model_name='validityrange',
            index=models.Index(fields=['date_start', 'date_end'], name='validity_date_start_date_end'),
        ),
    ]
