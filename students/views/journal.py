# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

def index(request):
	return render(request, 'students/journal.html', {})