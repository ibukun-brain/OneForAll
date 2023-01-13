from django.urls import path
from home import views as home_views
from home import htmx_views, ajax_views

app_name = "home"

urlpatterns = [
    path(
    "",
    view=home_views.IndexView.as_view(),
    name="index"
    ),
    path(
        "profile/<slug:slug>/",
        view=home_views.ProfileView.as_view(),
        name="profile",
    ),
    path(
        "account-settings/",
        view=home_views.UpdateAccountSettingsView.as_view(),
        name="update-account"
    ),
    path(
        "account-settings/change-password/",
        view=home_views.CustomPasswordChangeView.as_view(),
        name="password-change-view"
    ),
    path(
        'profile-about/<slug:slug>/',
        view=home_views.ProfileAboutView.as_view(),
        name="about-profile"
    ),
     path(
        'connections/<slug:slug>/',
        view=home_views.ConnectionsView.as_view(),
        name="connections"
    ),
    path(
        'update-profile-image/', 
        view=ajax_views.UpdateProfileImageView.as_view(), name="update-profile-image"
    ),
    path(
        'delete-profile-image/', 
        view=ajax_views.DeleteProfileImageView.as_view(), 
        name="delete-profile-image",
    )
    # path(
    #     '<slug:slug>/profile-about/',
    #     view=htmx_views.AboutHTMXView.as_view(),
    #     name="about-profile"
    # )
    # path(
    #     '<slug:slug>/profile-about/',
    #     view=htmx_views.ConnectionHTMXView.as_view(),
    #     name="about-profile"
    # )
]