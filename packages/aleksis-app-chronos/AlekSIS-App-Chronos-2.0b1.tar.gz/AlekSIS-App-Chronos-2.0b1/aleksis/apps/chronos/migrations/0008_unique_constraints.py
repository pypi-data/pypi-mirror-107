# Generated by Django 3.2.3 on 2021-05-22 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chronos', '0007_more_permissions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chronosglobalpermissions',
            options={'managed': False, 'permissions': (('view_all_room_timetables', 'Can view all room timetables'), ('view_all_group_timetables', 'Can view all group timetables'), ('view_all_person_timetables', 'Can view all person timetables'), ('view_timetable_overview', 'Can view timetable overview'), ('view_lessons_day', 'Can view all lessons per day'))},
        ),
        migrations.AlterField(
            model_name='room',
            name='short_name',
            field=models.CharField(max_length=255, verbose_name='Short name'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Long name'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='short_name',
            field=models.CharField(max_length=255, verbose_name='Short name'),
        ),
        migrations.AlterField(
            model_name='timeperiod',
            name='weekday',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Montag'), (1, 'Dienstag'), (2, 'Mittwoch'), (3, 'Donnerstag'), (4, 'Freitag'), (5, 'Samstag'), (6, 'Sonntag')], verbose_name='Week day'),
        ),
        migrations.AlterUniqueTogether(
            name='lessonsubstitution',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='timeperiod',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='validityrange',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='absencereason',
            constraint=models.UniqueConstraint(fields=('site_id', 'short_name'), name='unique_short_name_per_site_absence_reason'),
        ),
        migrations.AddConstraint(
            model_name='break',
            constraint=models.UniqueConstraint(fields=('site_id', 'short_name'), name='unique_short_name_per_site_break'),
        ),
        migrations.AddConstraint(
            model_name='lessonsubstitution',
            constraint=models.UniqueConstraint(fields=('lesson_period', 'week'), name='unique_period_per_week'),
        ),
        migrations.AddConstraint(
            model_name='room',
            constraint=models.UniqueConstraint(fields=('site_id', 'short_name'), name='unique_short_name_per_site_room'),
        ),
        migrations.AddConstraint(
            model_name='subject',
            constraint=models.UniqueConstraint(fields=('site_id', 'short_name'), name='unique_short_name_per_site_subject'),
        ),
        migrations.AddConstraint(
            model_name='subject',
            constraint=models.UniqueConstraint(fields=('site_id', 'name'), name='unique_name_per_site'),
        ),
        migrations.AddConstraint(
            model_name='supervisionarea',
            constraint=models.UniqueConstraint(fields=('site_id', 'short_name'), name='unique_short_name_per_site_supervision_area'),
        ),
        migrations.AddConstraint(
            model_name='timeperiod',
            constraint=models.UniqueConstraint(fields=('weekday', 'period', 'validity'), name='unique_period_per_range'),
        ),
        migrations.AddConstraint(
            model_name='validityrange',
            constraint=models.UniqueConstraint(fields=('school_term', 'date_start', 'date_end'), name='unique_dates_per_term'),
        ),
    ]
