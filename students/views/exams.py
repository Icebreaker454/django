# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from ..models.exam import Exam

def index(request):
	
	exams_list = Exam.objects.all()

	return render(request, 'students/exams_view.html',
		{
			'exams_list': exams_list,
		}
	)

def add(request):
	return HttpResponse('<h1>Add Exam Template</h1>')

def edit(request, eid):
	return HttpResponse('<h1>Edit exam %s Template</h1>' % eid)

def delete(request, eid):
	return HttpResponse('<h1>Remove exam %s Template</h1>' % eid)