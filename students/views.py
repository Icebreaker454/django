# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

#def students_list(request):
#	template = loader.get_template('index.html')
#	context = RequestContext(request, {})
#	return HttpResponse(template.render(context))
#EXACTLY THE SAME!

# Views for students

def students_list(request):
	students = (
		{'id': 1,
		 'first_name': u'Павло',
		 'last_name': u'Пукач',
		 'ticket': 1488,
		 'image': 'img/zoncolorBright.png'},
		{'id': 2,
		 'first_name': u'Віктор',
		 'last_name': u'Садовий',
		 'ticket': 1489,
		 'image': 'img/zoncolorMono.png'},
		)
	return render(request, 'students/students_view.html', {'students': students})
def students_add(request):
	return HttpResponse('<h1>Student add form</h1>')
def students_edit(request, sid):
	return HttpResponse('<h1>Edit Student %s</h1>' % sid)
def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' % sid)

#views for groups

def groups_list(request):
	return render(request, 'students/group_view.html', {})
def groups_add(request):
	return HttpResponse('<h1>Group add form</h1>')
def groups_edit(request, gid):
	return HttpResponse('<h1>Edit Group %s </h1>' % gid)
def groups_delete(request, gid):
	return HttpResponse('<h1>Delete Group %s </h1>' % gid)