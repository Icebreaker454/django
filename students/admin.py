# -*- coding: utf-8 -*-

from django.contrib import admin
from .models.student import Student
from .models.group import Group
from .models.exam import Exam
from .models.journal import MonthJournal
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.forms import ModelForm

# Register your models here.

class StudentFormAdmin(ModelForm):
    
    def clean_student_group(self):
        """
        Check whether the student is a group leader and raise a ValidationError
        if that group differs from the student group
        """
        groups = Group.objects.filter(leader = self.instance)
        
        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(
                u"Студент уже є старостою іншої групи", 
                code='invalid')
            
        return self.cleaned_data['student_group']

class StudentAdmin(admin.ModelAdmin):
    """Class for managing the Student model on admin site"""        
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']
    form = StudentFormAdmin
    
    def view_on_site(self, obj):
        return reverse('students_edit', kwargs={'pk': obj.id})
    
class GroupFormAdmin(ModelForm):
    """Adds custom validation to some admin fields"""
    
    def clean_leader(self):
        """
        Check whether the group leader belongs to the group itself
        """
        if self.cleaned_data['leader']:
            students = Student.objects.filter(student_group = self.instance)
            if self.cleaned_data['leader'] not in students:
                raise ValidationError(
                                      u'Студент не належить до групи',
                                      code = 'invalid')
                return self.cleaned_data['leader']
    
class GroupAdmin(admin.ModelAdmin):
    """Class for managing the Group model on admin site"""
    list_display = ['title', 'leader']
    list_display_links = ['title']
    list_per_page = 10
    search_fields = ['title', 'leader', 'notes']
    form = GroupFormAdmin
    
    def view_on_site(self, obj):
        return reverse('groups_edit', kwargs={'pk': obj.id})

admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Exam)
admin.site.register(MonthJournal)
