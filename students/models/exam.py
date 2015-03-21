# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse


class Exam(models.Model):
    """Exam model"""

    def get_absolute_url(self):
        return reverse('exams', kwargs={'pk': self.pk})

    def __unicode__(self):
        return "%s (%s)" % (self.course_name, self.exam_group.title)

    class Meta(object):
        verbose_name = u'Іспит'
        verbose_name_plural = u'Іспити'

    course_name = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        verbose_name=u"Назва предмету"
    )

    exam_date = models.DateTimeField(
        blank=False,
        null=False,
        verbose_name=u"Дата і час проведення"
    )

    exam_teacher = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"Викладач"
    )

    exam_group = models.ForeignKey(
        'Group',
        verbose_name=u"Група"
    )

