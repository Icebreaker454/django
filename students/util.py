# -*- coding: utf-8 -*-

"""
    Pagination module

    Created by: Icebreaker 
"""


from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage

def paginate(objects, size, request, context, var_name='object_list'):
    """ 
        Paginate objects provided by view 

        Arguments:
            * List of elements;
            * Number of objects per page;
            * Request to get url parameters;
            * Context to set new variables into;
            * Variable name for list of objects.

        Returns:
            > Updated context object.
    """

    paginator = Paginator(objects, size)

    page = request.GET.get('page', '1')
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    context[var_name] = object_list
    context['is_paginated'] = object_list.has_other_pages()
    context['page_obj'] = object_list
    context['paginator'] = paginator

    return context