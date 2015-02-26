# -*- coding: utf-8 -*-

from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from studentsdb.settings import ADMIN_EMAIL

class ContactForm(forms.Form):

	def __init__(self, *args, **kwargs):

		super(ContactForm, self).__init__(*args, **kwargs)
 	   	# This helper allows to customize the form 
		
	    	self.helper = FormHelper()
		# Form tag attributes
		self.helper.form_class = 'form-horizontal'
		self.helper.form_method = 'post'
		self.helper.form_action = reverse('contact_admin')

		# Twitter Bootstrap stypes
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'
		# Adding the 'Submit' button
		self.helper.add_input(Submit('send_button', u"Надіслати"))

	from_email = forms.EmailField(label=u"Ваша електронна адреса")
	subject = forms.CharField(label=u"Заголовок листа", max_length=128)
	message = forms.CharField(label=u"Текст повідомлення", widget=forms.Textarea)
	
	


		
		
   	
def index(request):
	# Check if form was posted
	if request.method == 'POST':
		# creating a form with the POST data
		form = ContactForm(request.POST)

		if form.is_valid():
			from_email = form.cleaned_data['from_email']
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']

			try:
				send_mail(subject, message, from_email, [ADMIN_EMAIL])
			except Exception:
				message = u"Під час відправки листа виникла непередбачувана помилка, спробуйте \
				скористатися сервісом трохи згодом"
			else:
				message = u"Повідомлення успішно надіслано!"

			return HttpResponseRedirect(
				u"%s?status_message=%s" % (reverse('contact_admin'), message)
			)
	# If the request is not POST, render empty form
	else:
		form = ContactForm()

	return render(request, 'contact_admin/form.html', {'form': form})
