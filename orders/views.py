import stripe

from django.http import HttpResponseRedirect, Http404 
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from django.conf import settings

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('login')
    for menu in Menu.objects.all():
        for section in menu.sections.all():
            context = {
                "user": request.user,
                "menus": Menu.objects.all(),
                "sections": menu.sections.all(),
                'menuitems:': section.get_menuitem()
            }
    return render(request, "orders/main.html", context)

# join the website
def join(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(index)
    else:
        form = RegisterForm()
    return render(request, "registration/join.html", {'form': form})

# show all menus
@login_required(login_url='/login')
def menu(request, menu_id):
    try:
        menu = Menu.objects.get(pk=menu_id)
        sections = menu.sections.all()
    except Menu.DoesNotExist:
        raise Http404("Menu does not exist")
    for section in sections:
        menuitems = section.menuitems.all()
        context = {
            "menu": menu,
            "sections": sections,
            "menuitems": menuitems
        }
        return render(request, "orders/menu.html", context)

#show all sections in selected menu
@login_required(login_url='/login')
def section(request, menu_id, section_id):
    try:
        user = request.user
        Cart.create_cart(user)
        menu = Menu.objects.get(pk=menu_id)
        section = Section.objects.get(pk=section_id)
        sections = Section.objects.all()
        menuitemname = section.get_menuitemname() # dont need
        items = set(menuitemname).intersection(Item.objects.all()) # dont need
        menuitems = section.menuitems.all().order_by('item', 'size')
        toppings = Topping.objects.all()
        cart = Cart.objects.get(user=user, current_status=True)
        orders = cart.orders.filter(user=user.id)
        key = settings.STRIPE_PUBLISHABLE_KEY
    except Section.DoesNotExist:
        raise Http404("Section does not exist")
    context = {
        "menu": menu,
        "section": section,
        "sections": sections,
        "items": items,
        "menuitems": menuitems,
        "orders": orders,
        "toppings": toppings,
        "cart": cart,
        "key": key,
    }
    return render(request, "orders/section.html", context)

#add users address found in section view
@login_required(login_url='/login')
def add_address(request, menu_id, section_id):
    try:
        user = request.user
        street = request.POST['street']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zipcode']
    except KeyError:
        pass
    Address.objects.create(user=user, street=street, city=city, state=state, zipcode=zipcode)
    return HttpResponseRedirect(reverse('section', args=(menu_id, section_id,)))

#create/customize the order 
@login_required(login_url='/login')
def create(request, menu_id, section_id, item_id):
    try:
        user = request.user
        menuitem = menuItem.objects.get(pk=item_id)
        orders = Order.objects.filter(user=user.id)
        section = Section.objects.get(pk=section_id)
        toppings = Topping.objects.all()
        substopping = subsTopping.objects.all()
        extras = Extra.objects.all()
    except KeyError:
        pass
    context = {
        'user': user,
        'section': section,
        'menuitem': menuitem,
         "orders": orders,
        "toppings": toppings,
        "substopping": substopping,
        "extras": extras
    }
    return render(request, "orders/create.html", context)

# add order to existing cart or create new cart
@login_required(login_url='/login')
def add(request):
    try:
        user = request.user
        item_id = request.POST['menuItem']
        menuitem = menuItem.objects.get(pk=item_id)
        count = request.POST['count']
        toppings = request.POST.getlist('topping')
        subtoppings = request.POST.getlist('subtopping')
        extra = request.POST.getlist('extra')
        section_id = menuitem.section.id
        menu_id = menuitem.section.menu.id
    except KeyError:
        pass
    new = Order.objects.create(user=user, menuItem=menuitem, count=count)
    new.save()
    neworder = Order.objects.get(pk=new.id)
    if toppings is not None:
        neworder.toppings.set(toppings)
    if subtoppings is not None:
        neworder.subsToppings.set(subtoppings)
    if extra is not None:
        neworder.extras.set(extra)
    cartid = Cart.create_cart(user)
    if cartid:
        cart = Cart.objects.get(pk=cartid)
        cart.orders.add(neworder)
    else: 
        cart = Cart.objects.get(user=user, current_status=True)
        cart.orders.add(neworder)
    return HttpResponseRedirect(reverse('section', args=(menu_id, section_id)))

# delete order
@login_required(login_url='/login')
def delete(request, menu_id, section_id, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except KeyError:
        return redirect(index)
    except Order.DoesNotExist:
        return redirect(index)
    order.delete()
    return HttpResponseRedirect(reverse('section', args=(menu_id, section_id,)))

#checkout using stripe and update cart database
@login_required(login_url='/login')
def checkout(request, cart_id):
    if request.method == "POST":
        stripe.api_key = settings.STRIPE_SECRET_KEY
        cart = Cart.objects.get(pk=cart_id)
        instruction = request.POST['instructions']
        orderOption = request.POST['orderOption']
        charge = stripe.Charge.create(
            amount=int(cart.stripe_total()),
            currency='usd',
            description='Pinocchios Pizza & Subs',
            source=request.POST['stripeToken'],
        )
        cart.option = str(orderOption)
        cart.instructions = str(instruction)
        cart.current_status = False
        cart.save()
        return render(request, 'orders/checkout/checkout.html')

#admin order view
def orders(request):
    if request.user.is_staff:
        carts = Cart.objects.all()
        context = {
            'carts': carts
        }  
        return render(request, "orders/staff/orders.html", context)
    else:
        return redirect(index)