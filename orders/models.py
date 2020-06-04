from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

class Address(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="address", blank=True)
    street = models.CharField(max_length=64, blank=True)
    city = models.CharField(max_length=64, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zipcode = models.IntegerField(blank=True)

    def __str__(self):
        return f"{self.user}, Street: {self.street}, city: {self.city}, state: {self.state}, zipcode: {self.zipcode}"

class Menu(models.Model):
    name = models.CharField(max_length=64)
    photo = models.ImageField(upload_to='static/img/', null=True, blank=True)

    def __str__(self):
        return f"Menu - {self.name}"

class Section(models.Model): # Menu.sections.all() for each section.menuitems.all()
    name = models.CharField(max_length=64)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="sections")
    photo = models.ImageField(upload_to='static/img/', null=True, blank=True)

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
    toppingCount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}, {self.hasToppings}, {self.toppingCount}"

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
        return f"{self.id} - {self.item} in {self.section}, Style: {self.style}, Size {self.size}, Price {self.price}"

class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class subsTopping(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.name} costs {self.price}"

class Extra(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} costs {self.price}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", blank=True, null=True)
    menuItem = models.ForeignKey(menuItem, on_delete=models.CASCADE, null=True)
    toppings = models.ManyToManyField(Topping, blank=True)
    subsToppings = models.ManyToManyField(subsTopping, blank=True)
    extras = models.ManyToManyField(Extra, blank=True)
    count = models.IntegerField()

    def topping_cost(self):
        return sum([round(topping.price * self.count, 2) for topping in self.toppings.all()])

    def subtopping_cost(self):
        return sum([round(subtopping.price * self.count, 2) for subtopping in self.subsToppings.all()])
    
    def extras_cost(self):
        return sum([round(extra.price * self.count, 2) for extra in self.extras.all()])

    def order_cost(self):
        return sum([round((self.menuItem.price + self.topping_cost() + self.subtopping_cost() + self.extras_cost()) * self.count, 2)])

    def __str__(self):
        return f"{self.id}: Order for {self.user} - Toppings: {self.toppings}, {self.count} {self.menuItem}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    orders = models.ManyToManyField(Order, blank=True)
    date = models.DateTimeField(timezone.now())
    current_status = models.BooleanField(default=True)
    orderOption = [
        ('PU', 'Pick up'),
        ('DL', 'Delivery')
    ]
    option = models.CharField(max_length=64, choices=orderOption, default='PU')
    instructions = models.TextField(max_length=300, blank=True)

    def create_cart(user):
        if not Cart.objects.filter(user=user):
            newcart = Cart.objects.create(user=user, date=timezone.now())
        elif not Cart.objects.filter(user=user, current_status=True):
            newcart = Cart.objects.create(user=user, date=timezone.now())
        
    def cart_total(self): # 2 decimal places
         return sum([round(order.menuItem.price * order.count + order.subtopping_cost() + order.extras_cost(), 2) for order in self.orders.all()])

    def stripe_total(self):
         return sum([round(order.menuItem.price * order.count + order.subtopping_cost() + order.extras_cost(), 2) * 100 for order in self.orders.all()])   

    def __str__(self):
        return f"For {self.user} ordered on {self.date}, Status: {self.current_status}, Option: {self.option}"
