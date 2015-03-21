# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin


from .settings import DEBUG, MEDIA_ROOT
from students.views.students import StudentUpdate
from students.views.students import StudentDelete
from students.views.groups import GroupUpdateView
from students.views.groups import GroupDeleteView
from students.views.journal import JournalView
from students.views.students import StudentView
from students.views.groups import GroupView
from students.views.exams import ExamView
from students.views.exams import ExamAddView
from students.views.exams import ExamUpdateView
from students.views.exams import ExamDeleteView

urlpatterns = patterns(
    '',
    # Students urls
    url(r'^$', StudentView.as_view(), name='home'),
    url(r'^students/add$', 'students.views.students.add', name='add_student'),
    url(r'^students/(?P<pk>\d+)/edit$', StudentUpdate.as_view(), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete$', StudentDelete.as_view(), name='students_delete'),

    # Groups urls
    url(r'^groups/$', GroupView.as_view(), name='groups'),
    url(r'^groups/add$', 'students.views.groups.add', name='add_group'),
    url(r'^groups/(?P<pk>\d+)/edit$', GroupUpdateView.as_view(), name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete$', GroupDeleteView.as_view(), name='groups_delete'),

    # Journal urls
    url(r'^journal/(?P<pk>\d+)?/?', JournalView.as_view(), name="journal"),

    # Exams urls
    url(r'^exams/$', ExamView.as_view(), name='exams'),
    url(r'^exams/add$', ExamAddView.as_view(), name='exams_add'),
    url(r'^exams/(?P<pk>\d+)/edit$', ExamUpdateView.as_view(), name='exams_edit'),
    url(r'^exams/(?P<pk>\d+)/delete$', ExamDeleteView.as_view(), name='exams_delete'),

    # Admin contact url
    url(r'^contact_admin/$', 'students.views.contact_admin.index', name='contact_admin'),

    # Admin url
    url(r'^admin/', include(admin.site.urls)),
)

if DEBUG:
    urlpatterns += patterns(
        '',
        url(
            r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': MEDIA_ROOT}
        )
    )
