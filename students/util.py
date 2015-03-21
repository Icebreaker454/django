# -*- coding: utf-8 -*-

"""
    Utility functions module

    Created by: Icebreaker 
"""

from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage


def get_groups(request):
    """ 
        This function returns the list of all groups
        to display on every template
    """
    # Deferred import to avoid cycle imports
    from .models.group import Group

    curr_group = get_current_group(request)

    groups = []
    for group in Group.objects.order_by('title'):
        groups.append(
            {
                'title': group.title,
                'id': group.id,
                'leader': group.leader and (
                    u'%s %s' %
                    (
                        group.leader.first_name,
                        group.leader.last_name
                    )
                ) or None,
                'selected': curr_group and curr_group.id == group.id
                and True or False
            }
        )

    return groups


def get_current_group(request):
    """
        This function returns currently selected group 
        from a request, or None
    """
    pk = request.COOKIES.get('current_group')

    if pk:
        from .models.group import Group

        try:
            group = Group.objects.get(pk=int(pk))
        except Group.DoesNotExist:
            return None
        else:
            return group
    else:
        return None


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