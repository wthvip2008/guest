"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from sign import views

urlpatterns = [
    path(r'', views.index),
    path('admin/', admin.site.urls),
    path(r'index/', views.index),
    path(r'logout/', views.logout),
    path(r'login_action/', views.login_action),
    path(r'event_manage/', views.event_manage),
    path(r'accounts/login/', views.index),
    path(r'search_name', views.search_name),
    path(r'guest_manage/', views.guest_manage),
    # path(r'sign_index/(?P<event_id>[0-9]+)/', views.sign_index),
    path('sign_index/<int:event_id>/', views.sign_index),
    path('sign_index2/<int:event_id>/', views.sign_index2),
    # path(r'sign_index2/(?P<event_id>[0-9]+)/', views.sign_index2),
    # path(r'sign_index_action/(?P<event_id>[0-9]+)/$', views.sign_index_action),
    path('sign_index_action/<int:event_id>/', views.sign_index_action),
]
        