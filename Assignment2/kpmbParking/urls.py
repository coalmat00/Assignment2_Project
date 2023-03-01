from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.index, name="index"),
    path("forgot_password", views.forgot_password, name="forgot_password"),
    path("register", views.register, name="register"),
    path("main_menu/", views.main_menu, name="main_menu"),
    path("logout/", views.logout, name="logout"),
    path(
        "main_menu/register_vehicle/", views.register_vehicle, name="register_vehicle"
    ),
    path("book_parking/", views.book_parking, name="book_parking"),
    path("main_menu/check_booking", views.check_booking, name="check_booking"),
    path("update_review/<str:booking_id>/", views.update_review, name="update_review"),
    path(
        "main_menu/personal_information",
        views.personal_information,
        name="personal_information",
    ),
    path(
        "update_personal_info", views.update_personal_info, name="update_personal_info"
    ),
    path("delete_account", views.delete_account, name="delete_account"),
    path("delete_review/<str:booking_id>", views.delete_review, name="delete_review"),
    path(
        "cancel_booking/<str:booking_id>", views.cancel_booking, name="cancel_booking"
    ),
]

urlpatterns += staticfiles_urlpatterns()
