# -*- coding: utf-8 -*-

from PIL import Image
from datetime import datetime

from django.forms import ModelForm
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import UpdateView, DeleteView
from ..models.student import Student
from ..models.group import Group

class StudentUpdateForm(ModelForm):
	class Meta:
		model = Student

	def __init__(self, *args, **kwargs):
		super(StudentUpdateForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		self.helper.form_action = reverse('students_edit', kwargs={'pk':kwargs['instance'].id})
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'

		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'

		self.helper.layout[-1] = FormActions(
			Submit('add_button', u"Зберегти", css_class="btn btn-primary"),
			Submit('cancel-button', u"Скасувати", css_class="btn btn-link"),
		)



#def students_list(request):
#	template = loader.get_template('index.html')
#	context = RequestContext(request, {})
#	return HttpResponse(template.render(context))
#EXACTLY THE SAME!

# Views for students

def list(request):
	students = Student.objects.order_by('last_name')
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
			errors = {}

			data = {
				'middle_name': request.POST.get('middle_name'),
				'notes': request.POST.get('notes')
			}	

			first_name = request.POST.get('first_name','').strip()
			if first_name:
				data['first_name'] = first_name
			else:
				errors['first_name'] = u"Ім'я є обов'язковим"

			last_name = request.POST.get('last_name','').strip()
			if last_name:
				data['last_name'] = last_name
			else:
				errors['last_name'] = u"Прізвище є обов'язковим"

			birthday = request.POST.get('birthday', '').strip()
			if not birthday:
				errors['birthday'] = u"Дата народження є обов'язковою"	
			else:
				try:
					datetime.strptime(birthday, '%Y-%m-%d')
				except Exception:
					errors['birthday'] = u"Дата повинна бути у вигляді РРРР-ММ-ДД"
				else:
					data['birthday'] = birthday

			
					

			ticket = request.POST.get('ticket','').strip()
			if ticket:
				data['ticket'] = ticket
			else:
				errors['ticket'] = u"Номер квитка є обов'язковим"

			student_group = request.POST.get('student_group', '').strip()
			if student_group:
				groups = Group.objects.filter(pk=student_group)
				if len(groups) != 1:
					errors['student_group'] = u"Оберіть коректну групу"
				else:
					data['student_group'] = groups[0]
			else:
				errors['student_group'] = u"Поле групи є обов'язковим"

			photo = request.FILES.get('photo')
			if photo:
				try:
					i = Image.open(photo)
					if i.size[0] > 1920 or i.size[1] > 1080:
						errors['photo'] = u"Розмір фото не повинен перевищувати 1920х1080"
					else:
						data['photo'] = photo
					
				except Exception:
					errors['photo'] = u"Файл непіходящого формату, або пошкоджений"
	

			# If there is no errors, we create a student from the user input
			if not errors:
				student = Student(**data)
				#	first_name = request.POST['first_name'],
				#	last_name = request.POST['last_name'],
				#	middle_name = request.POST['middle_name'],
				#	birthday = request.POST['birthday'],
				#	ticket = request.POST['ticket'],
				#	photo = request.FILES['photo'],
				#	student_group = Group.objects.get(pk = request.POST['student_group'])
				#)
				# Saving the student to database
				student.save()
				return HttpResponseRedirect(u"%s?status_message=Студента додано" % reverse('home'))

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
			return HttpResponseRedirect(u"%s?status_message=Зміни скасовано" % reverse('home'))
	# initial form render
	else:
		groups_list = Group.objects.all().order_by('title')

		return render(request, "students/students_add.html", 
			{
				'groups_list': groups_list
			}
		)	


class StudentUpdate(UpdateView):
	    model = Student
	    template_name = "students/students_edit.html"
	    form_class = StudentUpdateForm

	    def get_success_url(self):
	    	return u"%s?status_message=Студента успішно додано!" % reverse('home')

	    def post(self, request, *args, **kwargs):
	    	if request.POST.get('cancel_button'):
	    		return HttpResponseRedirect(u"%s?status_message=Редагування скасовано" % reverse('home'))
	    	else:
	    		return super(StudentUpdate, self).post(request, *args, **kwargs)

class StudentDelete(DeleteView):
		model = Student
		template_name = 'students/students_confirm_delete.html'

		def get_success_url(self):
			return u"%s?status_message=Студента успішно видалено!" % reverse('home')