"""MoneyGMA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from os import getenv
from django.conf import settings
from django.conf.urls.static import static


if getenv('MGMA_PREFIX_DOMAIN', "False") == "True":
    urlpatterns = [
        path('moneygma/admin/', admin.site.urls),
        path("moneygma/", include("App.urls")),
        path("moneygma/api/", include("Api.urls")),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns = [
        path('admin/', admin.site.urls),
        path("", include("App.urls")),
        path("api/", include("Api.urls")),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)