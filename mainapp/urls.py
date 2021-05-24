from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin

class LoginFormView(SuccessMessageMixin, LoginView):
    template_name='admin/login.html'
    success_message = "✔️ logged in successfully "

urlpatterns = [
    path('',views.homepage),
    path('details/',views.details),
    path('add-member/',views.add_member,name='add'),
    path('update/<int:id>/',views.update,name='update'),
    path('delete/',views.delete),
    path('login/',
        LoginFormView.as_view(
            extra_context={
                'site_header': 'Log in to Nidaghatta Family',
                'site_title' : 'login',
            })),
    path("logout/",views.logout),     
]
