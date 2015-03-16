# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_monthjournal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monthjournal',
            name='present_day0',
        ),
    ]
