# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_auto_20150207_1714'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': '\u0421\u0442\u0443\u0434\u0435\u043d\u0442', 'verbose_name_plural': '\u0421\u0442\u0443\u0434\u0435\u043d\u0442\u0438'},
        ),
        migrations.AlterField(
            model_name='student',
            name='birthday',
            field=models.DateField(null=True, verbose_name='\u0414\u0430\u0442\u0430 \u043d\u0430\u0440\u043e\u0434\u0436\u0435\u043d\u043d\u044f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(default=b'', max_length=256, verbose_name="\u0406\u043c'\u044f"),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(default=b'', max_length=256, verbose_name='\u041f\u0440\u0456\u0437\u0432\u0438\u0449\u0435'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='middle_name',
            field=models.CharField(default=b'', max_length=256, verbose_name='\u041f\u043e-\u0431\u0430\u0442\u044c\u043a\u043e\u0432\u0456', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='notes',
            field=models.TextField(default=b'', verbose_name='\u0414\u043e\u0434\u0430\u0442\u043a\u043e\u0432\u0456 \u043d\u043e\u0442\u0430\u0442\u043a\u0438', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(upload_to=b'', null=True, verbose_name='\u0424\u043e\u0442\u043e', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='student_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='\u0413\u0440\u0443\u043f\u0430', to='students.Group', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='ticket',
            field=models.CharField(default=b'', max_length=256, verbose_name='\u0411\u0456\u043b\u0435\u0442'),
            preserve_default=True,
        ),
    ]
