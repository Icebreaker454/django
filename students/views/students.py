# -*- coding: utf-8 -*-

from PIL import Image
from datetime import datetime

from django.forms import ModelForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.core.exceptions import ValidationError


from crispy_forms.bootstrap import FormActions
from crispy_forms.bootstrap import Div
from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from ..models.student import Student
from ..models.group import Group
from ..util import get_current_group


class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        self.helper.layout[3] = AppendedText(
            'birthday',
            '<span class="glyphicon glyphicon-calendar"></span>',
            active=True
        )

        self.helper.add_input(
            Submit('add_button', u"Зберегти", css_class="btn btn-primary")
        )
        self.helper.add_input(
            Submit('cancel-button', u"Скасувати", css_class="btn btn-link")
        )

    def clean_student_group(self):
        """
        Check whether the student is a group leader and raise a ValidationError
        if that group differs from the student group
        """
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(
                u"Студент уже є старостою іншої групи",
                code='invalid')
        return self.cleaned_data['student_group']


class StudentView(ListView):
    """ The students index view """
    template_name = 'students/students_view.html'
    context_object_name = "students"
    paginate_by = 6

    def get_queryset(self):

        current_group = get_current_group(self.request)

        if current_group:
            queryset = Student.objects.filter(student_group=current_group)
        else:
            queryset = Student.objects.all()

        order_by = self.request.GET.get('order_by', '')
        if order_by in ('first_name', 'last_name', 'ticket'):
            queryset = queryset.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                queryset = queryset.reverse()
        else:
            queryset = queryset.order_by('last_name')

        return queryset



def add(request):
    # Checking whether the method is Post
    if request.method == 'POST':
        # Checking if add button was clicked
        if request.POST.get('add_button') is not None:
            errors = {}

            data = {
                'middle_name': request.POST.get('middle_name'),
                'notes': request.POST.get('notes')
            }

            first_name = request.POST.get('first_name','').strip()
            if first_name:
                data['first_name'] = first_name
            else:
                errors['first_name'] = u"Ім'я є обов'язковим"

            last_name = request.POST.get('last_name','').strip()
            if last_name:
                data['last_name'] = last_name
            else:
                errors['last_name'] = u"Прізвище є обов'язковим"

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Дата повинна бути у вигляді РРРР-ММ-ДД"
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket','').strip()
            if ticket:
                data['ticket'] = ticket
            else:
                errors['ticket'] = u"Номер квитка є обов'язковим"

            student_group = request.POST.get('student_group', '').strip()
            if student_group:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u"Оберіть коректну групу"
                else:
                    data['student_group'] = groups[0]
            else:
                errors['student_group'] = u"Поле групи є обов'язковим"

            photo = request.FILES.get('photo')
            if photo:
                try:
                    i = Image.open(photo)
                    if i.size[0] > 1920 or i.size[1] > 1080:
                        errors['photo'] = u"Розмір фото не повинен перевищувати 1920х1080"
                    else:
                        data['photo'] = photo

                except Exception:
                    errors['photo'] = u"Файл непіходящого формату, або пошкоджений"

            # If there is no errors, we create a student from the user input
            if not errors:
                student = Student(**data)
                # Saving the student to database
                student.save()
                return HttpResponseRedirect(u"%s?status_message=Студента додано" % reverse('home'))

            # If we do have errors, we render the form with errors and previous user input
            else:
                return render(
                    request,
                    'students/students_add.html',
                    {
                        'groups_list': Group.objects.all().order_by('title'),
                        'errors': errors
                    }
                )
        # if the cancel button was pressed, redirect to home
        elif request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(u"%s?status_message=Зміни скасовано" % reverse('home'))
    # initial form render
    else:
        groups_list = Group.objects.all().order_by('title')

        return render(
            request,
            "students/students_add.html",
            {
                'groups_list': groups_list
            }
        )


class StudentUpdate(UpdateView):
        model = Student
        template_name = "students/students_edit.html"
        form_class = StudentUpdateForm

        def get_success_url(self):
            return u"%s?status_message=Студента успішно відредаговано!" % reverse('home')

        def post(self, request, *args, **kwargs):
            if request.POST.get('cancel_button'):
                return HttpResponseRedirect(u"%s?status_message=Редагування скасовано" % reverse('home'))
            else:
                return super(StudentUpdate, self).post(request, *args, **kwargs)


class StudentDelete(DeleteView):
        model = Student
        template_name = 'students/students_confirm_delete.html'

        def get_success_url(self):
            return u"%s?status_message=Студента успішно видалено!" % reverse('home')