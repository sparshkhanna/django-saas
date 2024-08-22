
from django.contrib import admin
from django.urls import path, include
from .views import home_view, about_view
from auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.login_view),
    path('register/', auth_views.register_view),
    path('hello-world/', home_view), # index page -> root page
    path('', home_view, name='home'),
    path('hello-world.html', home_view),
    path('accounts/', include('allauth.urls')), 
    path('about/', about_view),
   
]
 