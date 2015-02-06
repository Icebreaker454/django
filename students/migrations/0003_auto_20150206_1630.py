# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_student_notes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='birthday',
        ),
        migrations.RemoveField(
            model_name='student',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='student',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='student',
            name='middle_name',
        ),
        migrations.RemoveField(
            model_name='student',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='student',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='student',
            name='ticket',
        ),
    ]
