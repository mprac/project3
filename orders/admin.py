from django.contrib import admin
from . models import Menu, Section, Size, Style, Item, menuItem, Price, Topping, Order, Address, Cart

# Register your models here.
admin.site.register(Menu)
admin.site.register(Section)
admin.site.register(Size)
admin.site.register(Style)
admin.site.register(Item)
admin.site.register(Price)
admin.site.register(Topping)
admin.site.register(Order)
admin.site.register(menuItem)
admin.site.register(Address)
admin.site.register(Cart)
