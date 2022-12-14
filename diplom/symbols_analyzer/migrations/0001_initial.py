# Generated by Django 4.1.3 on 2022-11-18 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('students', models.PositiveSmallIntegerField(verbose_name='Количество студентов')),
                ('lessons', models.PositiveSmallIntegerField(verbose_name='Количество занятий')),
            ],
            options={
                'verbose_name': ('Журнал',),
                'verbose_name_plural': 'Журналы',
            },
        ),
    ]
