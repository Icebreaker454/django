# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from ..models.group import Group
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

#views for groups

def list(request):
	groupobj = Group.objects.all()
	order_by = request.GET.get('order_by', '')
	if  order_by in ('title', 'leader'):
		groupobj = groupobj.order_by(order_by)

		if request.GET.get('reverse', '') == '1':
			groupobj = groupobj.reverse()

	return render(
		request, 'students/group_view.html', 
		{
			'groupobj': groupobj,
		}
	)
def add(request):
	return HttpResponse('<h1>Group add form</h1>')
def edit(request, gid):
	return HttpResponse('<h1>Edit Group %s </h1>' % gid)
def delete(request, gid):
	return HttpResponse('<h1>Delete Group %s </h1>' % gid)
