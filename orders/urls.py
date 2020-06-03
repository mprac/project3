from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("join", views.join, name="join"),
    path("<int:menu_id>", views.menu, name="menu"),
    path("<int:menu_id>/<int:section_id>", views.section, name="section"),
    path("<int:menu_id>/<int:section_id>/<int:item_id>", views.create, name="create"),
    path("add/", views.add, name="add"),
    path("<int:menu_id>/<int:section_id>/<int:order_id>/delete", views.delete, name="delete"),
    path("<int:menu_id>/<int:section_id>/address", views.add_address, name="add_address"),
    path('checkout/<int:cart_id>', views.checkout, name='checkout'),
    path('orders', views.orders, name="orders"),
    
]

