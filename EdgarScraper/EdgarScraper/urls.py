"""EdgarScraper URL Configuration

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
from rest_framework import routers

from company.views import CompanyViewSet
from report_schema.views import RawReportViewSet, GeneratedReportViewSet

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='companies')
router.register(r'raw-reports', RawReportViewSet, basename='raw-reports')
router.register(r'generated-reports', GeneratedReportViewSet, basename='generated-reports')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls), name='api')
]
