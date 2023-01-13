"""ofa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView
)

urlpatterns = [
    path('user-session/', include('user_sessions.urls', 'user_sessions')),
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path(
        "account-settings/change-password-done/",
        view=PasswordChangeDoneView
        .as_view(template_name="account/change_password_done.html"),
        name="password_change_done"
    ),
    path("friends/", include('friends.urls', namespace="friends")),
    # path("<slug:slug>/", include('friends.urls', namespace="friends")),
    path("", include("home.urls", namespace="home")),


]



if settings.DEBUG:
    extra_patterns = [
    path('__debug__/', include('debug_toolbar.urls')),
]
    urlpatterns += static(
            settings.STATIC_URL,
            document_root=settings.STATIC_ROOT
        )
    urlpatterns += static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT
        )
    urlpatterns += extra_patterns
