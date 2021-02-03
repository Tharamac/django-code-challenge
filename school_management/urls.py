"""school_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from rest_framework_nested import routers
from school_manager import views

router = routers.SimpleRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'schools',views.SchoolViewSet)

school_router = routers.NestedSimpleRouter(router, r'schools', lookup= 'school')
school_router.register(r'students', views.StudentsListViewSet, basename= 'school-students')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
urlpatterns += school_router.urls
