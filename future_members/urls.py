from django.contrib import admin
from django.urls import path
from members import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home, name="home"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path("register/", views.register, name="register"),

    path(
        "member/<str:membership_number>/",
        views.member_detail,
        name="member_detail",
    ),

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
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
