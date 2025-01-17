"""transaction_task URL Configuration

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
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls.conf import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Promo System API",
        default_version="v1",
        description="Promo system",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path('', admin.site.urls),
    url(r'^api/', include('users.urls')),
    url(r'^api/', include('transaction.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'docs',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'
            ),
        url(r'redoc/$',
            schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'
            ),
    ]
