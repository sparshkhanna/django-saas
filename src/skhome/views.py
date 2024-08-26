from django.http import HttpResponse
from django.shortcuts import render
from visits.models import PageVisit
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings


LOGIN_URL = settings.LOGIN_URL




def home_view(request, *args, **kwargs ):

    return about_view(request, *args, **kwargs)


def about_view(request, *arsg, **kwargs):
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path=request.path)
    try:
        percent = (page_qs.count()*100.0)/qs.count()
    except:
        percent = 0 
    my_title = "My Page"
    html_template = "home.html"
    my_context = {
        "page_title" : my_title,
        "page_visit_count" : page_qs.count(),
        "percent" : percent,
        "total_visit_count" : qs.count()

    }
    
    PageVisit.objects.create(path=request.path)
    return render(request, html_template, my_context)





def my_old_home_page_view(request, *args, **kwargs ):
    my_title = "My Page"
    my_context = {
        "page_title" : my_title 
    }
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Saas</title>
</head>
<body>
    <h1>{my_title} anything</h1>
</body>
</html>""".format(**my_context)
    # html_file_path = this_dir / "home.html"
    # html_ = html_file_path.read_text()
    return HttpResponse(html)


VALID_CODE = "abc123"

def pw_protected_view(request, *args, **kwargs):
    is_allowed = request.session.get('protected_page_allowed') or 0
    
    if request.method == 'POST':
        user_pw_sent = request.POST.get('code') or None
        if user_pw_sent == VALID_CODE:
            is_allowed = 1
            request.session['protected_page_allowed'] = is_allowed
    if is_allowed:
        return render(request, 'protected/view.html', {})
    return render (request, 'protected/entry.html', {})


@login_required(login_url=LOGIN_URL)
def user_only_view(request, *args, **kwargs):
    return render(request, 'protected/user-only.html', {})

@staff_member_required(login_url=LOGIN_URL)
def staff_only_view(request, *args, **kwargs):
    return render(request, 'protected/staff-only.html', {})



