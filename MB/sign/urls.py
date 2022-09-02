from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import subscribe


urlpatterns = [
    path('logout/',
         LogoutView.as_view(template_name='sign/logout.html'),
         name='logout'),
    path('subscribe/', subscribe, name='subscribe'),
]
