"""
    This context processor is written for the main project

    Created by: Icebreaker
"""

def students_proc(request):
    """ Adds the absolute url and groups list to context """
    PORTAL_URL = request.scheme + '://' + request.get_host()
    return {
        'PORTAL_URL': PORTAL_URL,
    }

