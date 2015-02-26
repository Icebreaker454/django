from django.conf.urls import patterns, include, url
from django.contrib import admin
from .settings import DEBUG, MEDIA_ROOT
from students.views.students import StudentUpdate, StudentDelete
from students.views.groups import GroupUpdateView, GroupDeleteView

urlpatterns = patterns('',
    # Students urls
    url(r'^$', 'students.views.students.list', name='home'),
    url(r'^students/add$', 'students.views.students.add', name='add_student'),
    url(r'^students/(?P<pk>\d+)/edit$', StudentUpdate.as_view(), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete$', StudentDelete.as_view(), name='students_delete'),

    # Groups urls
    url(r'^groups/$', 'students.views.groups.list', name='groups'),
    url(r'^groups/add$', 'students.views.groups.add', name='add_group'),
    url(r'^groups/(?P<pk>\d+)/edit$', GroupUpdateView.as_view(), name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete$', GroupDeleteView.as_view(), name='groups_delete'),

    # Journal urls
    url(r'^journal/$', 'students.views.journal.index', name="journal"),

    # Exams urls
    url(r'^exams/$', 'students.views.exams.index', name="exams"),
    url(r'^exams/add$', 'students.views.exams.add', name="exams_add"),
    url(r'^exams/(?P<eid>\d+)/edit$', 'students.views.exams.edit', name='exams_edit'),
    url(r'^exams/(?P<eid>\d+)/delete$', 'students.views.exams.delete', name='exams_delete'),

    # Admin contact url
    url(r'^contact_admin/$', 'students.views.contact_admin.index', name='contact_admin'),

    # Admin url
    url(r'^admin/', include(admin.site.urls)),
)

if DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': MEDIA_ROOT }
        )
    )
