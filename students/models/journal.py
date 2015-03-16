# -*- coding: utf-8 -*-
"""
    This module is one of the models' modules
    PEP8_CONFIRMED
"""

from django.db import models


class MonthJournal(models.Model):
    """ The model for the students month journal """

    class Meta:
        """ Metadata for our model """
        verbose_name = u"Журнал відвідування"
        verbose_name_plural = u"Журнали відвідування"

    # The student, whose presence is checked
    student = models.ForeignKey(
        'Student',
        verbose_name=u"Студент",
        blank=False,
        # Make sure that this field is unique for each month
        unique_for_month='date'
        )
    # The month and year of student's presence checking
    date = models.DateField(
        verbose_name=u"Дата",
        blank=False
        )

    def __unicode__(self):
        """ String representation of our model """
        return '%s: %d, %d' % (
            self.student.last_name,
            self.date.month,
            self.date.year
            )

# Here we add 31
for i in range(1, 31):
    MonthJournal.add_to_class(
        'present_day%d' % (i),
        models.BooleanField(default=False)
        )
