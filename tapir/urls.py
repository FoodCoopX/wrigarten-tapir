"""tapir URL Configuration

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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from tapir.settings import ENABLE_SILK_PROFILING
from tapir.wirgarten.views.default_redirect import wirgarten_redirect_view

urlpatterns = [
    path("", wirgarten_redirect_view),
    path("admin/", admin.site.urls),
    path("accounts/", include("tapir.accounts.urls")),
    path("log/", include("tapir.log.urls")),
    path("config/", include("tapir.configuration.urls")),
    path("wirgarten/", include("tapir.wirgarten.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if ENABLE_SILK_PROFILING:
    urlpatterns += [url(r"^silk/", include("silk.urls", namespace="silk"))]
