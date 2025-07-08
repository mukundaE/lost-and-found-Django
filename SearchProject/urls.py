"""
URL configuration for SearchProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from SearchApp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/",views.home,name="home"),
    path("login/",views.login,name="login"),
    path("log_out/",views.log_out,name="log_out"),
    path("register/",views.register,name="register"),
    path("reportlost/",views.reportlost,name="reportlost"),
    path("reportfound/",views.reportfound,name="reportfound"),
    path("admin_home/",views.admin_home,name="admin_home"),
    path("found_list/",views.found_list,name="found_list"),
    path('lost_list/', views.lost_list, name='lost_list'),
    path('update_lost/<int:id>/', views.update_lost, name='update_lost'),
    path('update_found/<int:id>/',views.update_found,name="update_found"),
    path('delete_lost/<int:id>/',views.delete_lost,name="delete_lost"),
    path("delete_found/<int:id>/",views.delete_found,name="delete_found"),
    path("claim_item/<int:id>/",views.claim_item,name="claim_item"),
    path('claimdashboard/', views.claimdashboard, name='claimdashboard'),
    path('contact/',views.contact,name="contact")

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
