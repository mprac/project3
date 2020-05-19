from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="address")
    street = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zipcode = models.IntegerField(blank=True)

    def __str__(self):
        return f"{self.user}, Street: {self.street}, city: {self.city}, state: {self.state}, zipcode: {self.zipcode}"

class Menu(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"Menu - {self.name}"

class Section(models.Model): # Menu.sections.all() for each section.menuitems.all()
    name = models.CharField(max_length=64)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="sections")

    def get_menuitemname(self):
        return ([menuitem.item for menuitem in self.menuitems.all()])

    def get_menuitem(self):
         return ([menuitem for menuitem in self.menuitems.all()])
    

    def __str__(self):
        return f"Section - {self.name} in {self.menu} Menu"

class Style(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Item(models.Model):
    name = models.CharField(max_length=64)
    hasToppings = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

class menuItem(models.Model): # Section.menuitems.all()
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='menuitems')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='menuitems')
    style = models.ForeignKey(Style, on_delete=models.CASCADE, blank=True, null=True)
    sizeOptions = [
        ('Regular', 'Regular'),
        ('Small','Small'),
        ('Medium','Medium'),
        ('Large','Large')
    ]
    size = models.CharField(max_length=64, choices=sizeOptions, default='Regular')
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.item} in {self.section}, Style: {self.style}, Size {self.size}, Price {self.price}"

class Topping(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.name} costs {self.price}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", blank=True, null=True)
    menuItem = models.ForeignKey(menuItem, on_delete=models.CASCADE, null=True)
    toppings = models.ManyToManyField(Topping, blank=True)
    count = models.IntegerField()

    def topping_cost(self):
        return sum([round(topping.price * self.count, 2) for topping in self.toppings.all()])

    def __str__(self):
        return f"{self.id}: Order for {self.user} - Toppings: {self.toppings}, {self.count} {self.menuItem}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    orders = models.ManyToManyField(Order)
    date = models.DateTimeField(timezone.now())
    current_status = models.BooleanField(default=True)
    orderOption = [
        ('PU', 'Pick up'),
        ('DL', 'Delivery')
    ]
    option = models.CharField(max_length=64, choices=orderOption, default='PU')
    instructions = models.TextField(max_length=300, blank=True)

    def cart_total(self): # 2 decimal places
         return sum([round(order.menuItem.price * order.count + order.topping_cost(), 2) for order in self.orders.all()])

    def __str__(self):
        return f"For {self.user} ordered on {self.date}, Status: {self.current_status}, Option: {self.option}"
