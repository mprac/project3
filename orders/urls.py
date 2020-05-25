from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:menu_id>", views.menu, name="menu"),
    path("<int:menu_id>/<int:section_id>", views.section, name="section"),
    path("join", views.join, name="join"),
    path("<int:menu_id>/<int:section_id>/create", views.create, name="create"),
    path("<int:menu_id>/<int:section_id>/<int:order_id>", views.edit, name="edit"),
    path("<int:menu_id>/<int:section_id>/<int:order_id>", views.delete, name="delete"),
    # path("<int:menu_id>/<int:section_id>/<int:order_id>", views.update, name="update"),
    
]

