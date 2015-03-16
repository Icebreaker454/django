# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from calendar import weekday
from calendar import day_abbr

from django.http import HttpResponse
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView

from ..models.student import Student
from ..models.journal import MonthJournal
from ..util import paginate

class JournalView(TemplateView):
    """ The view class to display students month journal """
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        context = super(JournalView, self).get_context_data(**kwargs)

        # Checking whether we have to display a specific month
        if self.request.GET.get('month'):
            month = datetime.strptime(
                self.request.GET['month'],
                "%Y-%m-%d"
                ).date()
        # Otherwise just display the current month
        else:
            today = datetime.today()
            month = date(today.year, today.month, 1)

        # Calculate previous and next month details;
        # We have to use it in the navigation 
        next_month = month + relativedelta(months=1)
        prev_month = month - relativedelta(months=1)
        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['next_month'] = next_month.strftime('%Y-%m-%d')
        context['year'] = month.year
        context['month_verbose'] = month.strftime('%B')

        context['cur_month'] = month.strftime('%Y-%m-%d')

        myear, mmonth = month.year, month.month
        number_of_days = monthrange(myear, mmonth)[1]

        context['month_header'] = [
            {
                'day': d,
                'verbose': day_abbr[weekday(myear, mmonth, d)][:2]
            }
            for d in range(1, number_of_days+1)
        ]

        # Getting all students from database
        queryset = Student.objects.order_by('last_name')
        # Defining update url for AJAX methods
        update_url = reverse('journal')

        students = []
        # Now we go through the students and collecting presence data

        for student in queryset:
            # Try to get the journal for selected month
            try:
                journal = MonthJournal.objects.get(student=student, date=month)
            except Exception:
                journal = None

            # Fill days presence for current student
            days = []
            for day in range(1, number_of_days+1):
                days.append(
                    {
                        'day': day,
                        'present': journal and getattr(
                            journal,
                            'present_day%d' % (day),
                            False
                        ) or False,
                        'date': date(myear, mmonth, day).strftime('%Y-%m-%d')
                    }
                )
            # Prepare metadata for current student
            students.append(
                {
                    'fullname': u'%s %s' % (
                        student.last_name,
                        student.first_name
                        ),
                    'days': days,
                    'id': student.id,
                    'update_url': update_url
                }
            )

        # Apply pagination
        context = paginate(
            students,
            10,
            self.request,
            context,
            var_name='students'
        )

        # Return updated context with paginated students
        return context

    def post(self, request, *args, **kwargs):
        """ Method to trace and callback all POST requests """

        data = request.POST

        # Prepare student, dates and presence data
        current_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        month = date(current_date.year, current_date.month, 1)
        present = data['present'] and True or False
        student = Student.objects.get(pk=data['pk'])

        # Prepare your anus... or the journal
        # get_or_create returns the actual object and True\False;
        # depending on whether the object was got or created
        journal = MonthJournal.objects.get_or_create(
            student=student,
            date=month
            )[0]

        # Set the journal data
        setattr(journal, 'present_day%d' % current_date.day, present)
        journal.save()

        return JsonResponse({'status': 'success'})