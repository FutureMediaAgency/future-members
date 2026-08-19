from django.contrib import admin
from django.urls import path
from members import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
    path(
        "verify/<str:membership_number>/",
        views.verify,
        name="verify",
    ),
    path(
        "verify/<str:membership_number>/qr.svg",
        views.member_qr,
        name="member_qr",
    ),
]
