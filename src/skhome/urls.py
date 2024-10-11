
from django.contrib import admin
from django.urls import path, include
from auth import views as auth_views
from subscriptions import views as subscription_views
from .views import (home_view, 
                    about_view, 
                    pw_protected_view,
                    user_only_view,
                    staff_only_view)

 
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('login/', auth_views.login_view),
    # path('register/', auth_views.register_view),
    path('pricing/', subscription_views.subscription_price_view, name='pricing'),
    path('pricing/<str:interval>/', subscription_views.subscription_price_view, name='pricing_interval'),
    path('hello-world/', home_view), # index page -> root page
    path('', home_view, name='home'),
    path('hello-world.html', home_view),
    path('accounts/', include('allauth.urls')), 
    path('protected/', pw_protected_view),
    path('protected/user-only', user_only_view),
    path('protected/staff-only', staff_only_view),
    path('profiles/', include('profiles.urls')), 

   
]



     