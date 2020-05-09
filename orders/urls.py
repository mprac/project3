from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:menu_id>", views.menu, name="menu"),
    path("<int:menu_id>/<int:section_id>", views.section, name="section"),
    path("join/", views.join, name="join"),
]

