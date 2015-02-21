# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.student import Student
from ..models.group import Group

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
	# Checking whether the method is Post
	if request.method == 'POST':
		# Checking if add button was clicked 
		if request.POST.get('add_button') is not None:

			# TODO: Validate input from user
			errors = {}		

			# If there is no errors, we create a student from the user input
			if not errors:
				student = Student(
					first_name = request.POST['first_name'],
					last_name = request.POST['last_name'],
					middle_name = request.POST['middle_name'],
					birthday = request.POST['birthday'],
					ticket = request.POST['ticket'],
					photo = request.FILES['photo'],
					student_group = Group.objects.get(pk = request.POST['student_group'])
				)
				# Saving the dtudent to database
				student.save()
				return HttpResponseRedirect(reverse('home'))

			# If we do have errors, we render the form with errors and previous user input
			else:
				return render(request, 'students/students_add.html',
					{
						'groups_list': Group.objects.all().order_by('title'),
						'errors': errors
					}
				)
		# if the cancel button was pressed, redirect to home
		elif request.POST.get('cancel_button') is not None:
			return HttpResponseRedirect(reverse('home'))
	# initial form render
	else:
		groups_list = Group.objects.all().order_by('title')

		return render(request, "students/students_add.html", 
			{
				'groups_list': groups_list
			}
		)	
def edit(request, sid):
	return HttpResponse('<h1>Edit Student %s</h1>' % sid)
def delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' % sid)
