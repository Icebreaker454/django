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

def list(request):
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
def add(request):
	return HttpResponse('<h1>Student add form</h1>')
def edit(request, sid):
	return HttpResponse('<h1>Edit Student %s</h1>' % sid)
def delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' % sid)

