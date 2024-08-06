from django.http import HttpResponse
from django.shortcuts import render
from visits.models import PageVisit


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