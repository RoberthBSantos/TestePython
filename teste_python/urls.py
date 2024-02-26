"""
URL configuration for teste_python project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from rest_framework.routers import DefaultRouter

from accounts.auth_views import LoginAPIView
from accounts.views import UserViewSet
from companies.views import CompanyViewSet, CompanyMemberView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'companies', CompanyViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('company_member/add/', CompanyMemberView.as_view({'post': 'create'}), name='add-company-member'),
    path('my-companies/', CompanyMemberView.as_view({'get': 'get_companies'}), name='my-companies'),
    path('company/members/', CompanyMemberView.as_view({'post': 'get_members'}), name='members'),
]
