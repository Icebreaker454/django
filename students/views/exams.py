# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from ..models.exam import Exam


class ExamView(TemplateView):
    """
        The exams index view
    """
    template_name = 'students/exams_view.html'

    def get_context_data(self, **kwargs):
        context = super(ExamView, self).get_context_data(**kwargs)

        curr_group = self.request.COOKIES.get('current_group')

        if curr_group:
            exams = Exam.objects.filter(exam_group=curr_group)
        else:
            exams = Exam.objects.all()

        order_by = self.request.GET.get('order_by','')
        if order_by in ('exam_teacher', 'course_name', 'exam_date'):
            exams = exams.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                exams = exams.reverse()

        context['exams_list'] = exams

        return context


class ExamForm(ModelForm):
    class Meta:
        model = Exam

    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        if not kwargs['instance']:
            self.helper.form_action = reverse('exams_add')
        else:
            self.helper.form_action = reverse('exams_edit', kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        self.helper.add_input(
            Submit('add_button', u"Зберегти", css_class="btn btn-primary")
        )
        self.helper.add_input(
            Submit('cancel-button', u"Скасувати", css_class="btn btn-link")
        )


class ExamAddView(CreateView):
    """
        Exams add exam view
    """
    model = Exam
    template_name = 'students/exams_add_t.html'
    form_class = ExamForm

    def get_success_url(self):
        return u"%s?status_message=Іспит успішно додано" % reverse('exams')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel-button'):
            return HttpResponseRedirect(
                u'%s?status_message=Редагування скасовано' % reverse('exams')
            )
        else:
            return super(ExamAddView, self).post(request, *args, **kwargs)


class ExamUpdateView(UpdateView):
        """
            Exams update view
        """
        model = Exam
        template_name = 'students/exams_edit.html'
        form_class = ExamForm

        def get_success_url(self):
            return u"%s?status_message=Іспит успішно відредаговано" % reverse('exams')

        def post(self, request, *args, **kwargs):
            if request.POST.get('cancel-button'):
                return HttpResponseRedirect(
                    u"%s?status_message=Редагування іспиту скасовано" %
                    reverse('exams')
                )
            else:
                return super(ExamUpdateView, self).post(request, *args, **kwargs)


class ExamDeleteView(DeleteView):
        model = Exam
        template_name = 'students/exams_confirm_delete.html'

        def get_success_url(self):
            return u"%s?status_message=Іспит видалено" % reverse('exams')