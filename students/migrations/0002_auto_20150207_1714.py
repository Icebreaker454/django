# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'Student'},
        ),
        migrations.AlterField(
            model_name='student',
            name='birthday',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(default=b'', max_length=256),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(default=b'', max_length=256),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='middle_name',
            field=models.CharField(default=b'', max_length=256, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='notes',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='student_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='students.Group', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='ticket',
            field=models.CharField(default=b'', max_length=256),
            preserve_default=True,
        ),
    ]
