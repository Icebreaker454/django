# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.


class Student(models.Model):

    """Student model"""

    # METADATA

    class Meta(object):
        verbose_name = u"Студент"
        verbose_name_plural = u"Студенти"

    # MODEL FIELDS SECTION

    first_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Ім'я",
        default=''
    )
    last_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Прізвище",
        default=''
    )
    middle_name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"По-батькові",
        default=''
    )

    birthday = models.DateField(
        blank=True,
        verbose_name=u"Дата народження",
        null=True
    )
    student_group = models.ForeignKey(
        'Group',
        verbose_name=u'Група',
        blank=False,
        null=True,
        on_delete=models.PROTECT,
    )

    photo = models.ImageField(
        blank=True,
        verbose_name=u"Фото",
        null=True
    )

    ticket = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Білет",
        default=''
    )
    notes = models.TextField(
        blank=True,
        verbose_name=u"Додаткові нотатки",
        default=''
    )

    # UNICODE

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)
