# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.student import Student

#def students_list(request):
#	template = loader.get_template('index.html')
#	context = RequestContext(request, {})
#	return HttpResponse(template.render(context))
#EXACTLY THE SAME!

# Views for students

def list(request):
	students = Student.objects.all()
	#--------------------
	# LIST ORDERING
	#--------------------
	order_by = request.GET.get('order_by', '')

	if order_by in ('first_name', 'last_name', 'ticket'):
		students = students.order_by(order_by)

		if request.GET.get('reverse', '') == '1':
			students = students.reverse()
	#--------------------
	# END LIST ORDERING
	#--------------------
	# PAGINATE THE DATA
	#--------------------
	# VARIANT No.1
	#--------------------
	paginator = Paginator(students, 3)
	page = request.GET.get('page')
	try:
		students = paginator.page(page)
	except PageNotAnInteger:
		students = paginator.page(1)
	except EmptyPage:
	 	students = paginator.page(paginator.num_pages)
	#--------------------	
	# VARIANT No.2
	#--------------------
	# per_page = 3
	# pagestr = request.GET.get('page', '1')
	# if pagestr:
	#	page = int(pagestr)
	#	students = students[(page-1)*per_page:page*per_page]
	#	page_num = []
	#	for i in range(len(students) - 1):
	#		page_num.append(i)

	return render(request, 'students/students_view.html',
		{
			'students': students,
		}
	)
def add(request):
	return HttpResponse('<h1>Student add form</h1>')
def edit(request, sid):
	return HttpResponse('<h1>Edit Student %s</h1>' % sid)
def delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' % sid)
