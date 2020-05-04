from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

class Section(models.Model):
    name = models.CharField(max_length=64)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="sections")

    def __str__(self):
        return f"Section - {self.name} in {self.menu} Menu"

class Size(models.Model):
    size = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.size}"

class Style(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Item(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class menuItem(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='sections')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items')
    style = models.ForeignKey(Style, on_delete=models.CASCADE, related_name='styles', blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='sizes', blank=True, null=True)
    price = models.DecimalField(max_digits=4,decimal_places=2)
    
    def __str__(self):
        return f"{self.item} in {self.section}, Size: {self.size}, Style: {self.style}, Price: {self.price}"

class Topping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Price(models.Model):
    amount = models.DecimalField(max_digits=4,decimal_places=2)
    Topping = models.OneToOneField(Topping, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.Topping} costs {self.amount}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    menuItem = models.ForeignKey(menuItem, on_delete=models.CASCADE, null=True)
    toppings = models.ManyToManyField(Topping, blank=True)
    count = models.IntegerField()

    def __str__(self):
        return f"Order for {self.user} - {self.count} {self.menuItem}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    orders = models.ManyToManyField(Order, related_name='orders')
    date = models.DateTimeField(timezone.now())
    current_status = models.BooleanField(default=True)
    orderOption = [
        ('PU', 'Pick up'),
        ('DL', 'Delivery')
    ]
    option = models.CharField(max_length=64, choices=orderOption, default='PU')
    instructions = models.TextField(max_length=300, blank=True)

    def cart_total(self): # 2 decimal places
         return sum([round(order.menuItem.price * order.count, 2) for order in self.orders.all()])

    def __str__(self):
        return f"For {self.user} ordered on {self.date}, Status: {self.current_status}, Option: {self.option}"
