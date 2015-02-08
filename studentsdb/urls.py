from django.conf.urls import patterns, include, url
from django.contrib import admin
from .settings import DEBUG, MEDIA_ROOT

urlpatterns = patterns('',
    # Students urls
    url(r'^$', 'students.views.students.list', name='home'),
    url(r'^students/add$', 'students.views.students.add', name='add_student'),
    url(r'^students/(?P<sid>\d+)/edit$', 'students.views.students.edit', name='students_edit'),
    url(r'^students/(?P<sid>\d+)/delete$', 'students.views.students.delete', name='students_delete'),

    # Groups urls
    url(r'^groups/$', 'students.views.groups.list', name='groups'),
    url(r'^groups/add$', 'students.views.groups.add', name='groups_add'),
    url(r'^groups/(?P<gid>\d+)/edit$', 'students.views.groups.edit', name='groups_edit'),
    url(r'^groups/(?P<gid>\d+)/delete$', 'students.views.groups.delete', name='groups_delete'),

    # Journal urls
    url(r'^journal/$', 'students.views.journal.index', name="journal"),

    # Exams urls
    url(r'^exams/$', 'students.views.exams.index', name="exams"),
    url(r'^exams/add$', 'students.views.exams.add', name="exams_add"),
    url(r'^exams/(?P<eid>\d+)/edit$', 'students.views.exams.edit', name='exams_edit'),
    url(r'^exams/(?P<eid>\d+)/delete$', 'students.views.exams.delete', name='exams_delete'),

    # Admin url
    url(r'^admin/', include(admin.site.urls)),
)

if DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': MEDIA_ROOT }
        )
    )
