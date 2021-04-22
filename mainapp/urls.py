from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('',views.homepage),
    path('details/',views.details),
    path('addmember/',views.addmembers),
    path('login/',
        LoginView.as_view(
            template_name='admin/login.html',
            extra_context={
                'site_header': 'Log in to Nidaghatta Family',
                'site_title' : 'login',
            })),
    path("logout/",views.logout)        
]
