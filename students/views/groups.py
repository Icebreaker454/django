# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template import loader
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import TemplateView
from django.forms import ModelForm


from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Submit


from ..models.group import Group
from ..models.student import Student
from ..util import paginate

class GroupUpdateForm(ModelForm):
    class Meta:
        model = Group

    def __init__(self, *args, **kwargs):
        super(GroupUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.form_action = reverse(
                'groups_edit', 
				kwargs={
					'pk':kwargs['instance'].id
					}
			)
      	self.helper.form_method = 'POST'
     	self.helper.form_class = 'form-horizontal'
      	self.helper.help_text_inline = True
      	self.helper.html5_required = True
      	self.helper.label_class = 'col-sm-2 control-label'
      	self.helper.field_class = 'col-sm-10'
        self.helper.layout[-1] = FormActions(
      		Submit('add_button', u"Зберегти", css_class="btn btn-primary"),
       		Submit('cancel_button', u"Скасувати", css_class="btn btn-link"),
       	)
    
    def clean_leader(self):
        """
        Validation function to check whether the leader of the group
        belongs to the group itself
        """
        #If there's actually a leader specified...
        if self.cleaned_data['leader']:
            if self.cleaned_data['leader'] not in Student.objects.filter(student_group=self.instance):
                raise ValidationError(
                    u"Студент не належить даній групі",
                    code = 'invalid')
            return self.cleaned_data['leader']    
       
class GroupView(TemplateView):
    """ The group's index view """

    template_name = 'students/group_view.html'

    def get_context_data(self, **kwargs):
        context = super(GroupView, self).get_context_data(**kwargs)

        groups = Group.objects.all()

        order_by = self.request.GET.get('order_by', '')
        if  order_by in ('title', 'leader'):
            groups = groups.order_by(order_by)
            if self.request.GET.get('reverse', '') == '1':
                groups = groups.reverse()

        context = paginate(groups, 3, self.request, context, var_name='groupobj')

        return context


def add(request):
    if request.method == 'POST':
        if request.POST.get('add_button') is not None:

            data = {'notes': request.POST.get('notes')}
            errors = {}

            title = request.POST.get('title', '').strip()
            if not title:
                errors['title'] = u"Це поле є обов'язковим"
            else:
                data['title'] = title

            leader = request.POST.get('leader').strip()
            if leader:
                leaders = Student.objects.filter(pk=leader)
                if len(leaders) > 1:
                    errors['leader'] = u"Виберіть коректного студента"
                else:
                    groups = Group.objects.filter(leader=leaders[0])
                    if len(groups) > 0:
                        raise ValidationError(
                            u"Цей студент уже є старостою іншої групи",
                            code='invalid'
                            )
            if not errors:
                group = Group(**data)
                group.save()

                if leader:
                    leaders = Student.objects.filter(pk=leader)
                    leaders[0].group = group
                    leaders[0].save()

                return HttpResponseRedirect(u"%s?status_message=Групу успішно додано" % reverse('groups'))
            else:
                students_list = Student.objects.order_by('last_name')
                return render(request, 'students/group_add.html', {'errors': errors, 'students_list': students_list})

        if request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(u"%s?status_message=Зміни скасовано" % reverse('groups'))


    else:
        students_list = Student.objects.order_by('last_name')
        return render(request, 'students/group_add.html', {'students': students_list})


class GroupUpdateView(UpdateView):
    model = Group
    template_name = "students/group_edit.html"
    form_class = GroupUpdateForm

    def get_success_url(self):
        return u"%s?status_message=Групу успішно відредаговано" % reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u"%s?status_message=Зміни скасовано" % reverse('home'))
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs)

class GroupDeleteView(DeleteView):
    model = Group
    template_name = "students/group_confirm_delete.html"

    def get_success_url(self):
        return u"%s?status_message=Групу успішно видалено" % reverse('groups')
