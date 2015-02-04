# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

#views for groups

def list(request):
	return render(request, 'students/group_view.html', {})
def add(request):
	return HttpResponse('<h1>Group add form</h1>')
def edit(request, gid):
	return HttpResponse('<h1>Edit Group %s </h1>' % gid)
def delete(request, gid):
	return HttpResponse('<h1>Delete Group %s </h1>' % gid)