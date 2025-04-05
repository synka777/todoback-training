"""
URL configuration for todoback project.

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
from django.urls import path, include
from api import views

urlpatterns = [
    #path("admin/", admin.site.urls),
    # path("api/", include("api.urls"))
    path("tasks/create/", views.task_create, name="task_create"),
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/<int:pk>", views.task_detail, name="task_detail"),
    path("tasks/update/<int:pk>", views.task_update, name="task_update"),
    path("tasks/delete/<int:pk>", views.task_delete, name="task_delete"),

    # No authentication needed
    path("login/", views.login_view),
    path("register/", views.register_view)
]
