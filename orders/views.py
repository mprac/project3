from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpRequest, JsonResponse 
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie, requires_csrf_token, csrf_protect
from django.views.decorators.vary import vary_on_headers
from django.template import RequestContext
from django.core import serializers

# () tuple - a collection which is ordered and changeable. allows duplicate
# [] list - a collection which is ordered and unchangeable. allows duplicate
# {} set - a collection which is unordered and unindexed. no duplicates
# {} dictionary - is a collection which is unordered changeable and indexed.no duplicates

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

def join(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(index)
    else:
        form = RegisterForm()
    return render(request, "registration/join.html", {'form': form})

@login_required(login_url='/login')
def menu(request, menu_id):
    try:
        menu = Menu.objects.get(pk=menu_id)
        sections = menu.sections.all()
    except Menu.DoesNotExist:
        raise Http404("Menu does not exist")
    context = {
        "menu": menu,
        "sections": sections,
    }
    return render(request, "orders/menu.html", context)

@login_required(login_url='/login')
def section(request, menu_id, section_id):
    try:
        user = request.user
        menu = Menu.objects.get(pk=menu_id)
        section = Section.objects.get(pk=section_id)
        menuitemname = section.get_menuitemname() # dont need
        items = set(menuitemname).intersection(Item.objects.all()) # dont need
        menuitems = section.menuitems.all().order_by('item', 'size')
        orders = Order.objects.filter(user=user.id)
        toppings = Topping.objects.all()
    except Section.DoesNotExist:
        raise Http404("Section does not exist")
    context = {
        "menu": menu,
        "section": section,
        "items": items,
        "menuitems": menuitems,
        "orders": orders,
        "toppings": toppings,
    }
    return render(request, "orders/section.html", context)

@login_required(login_url='/login')
def create(request, menu_id, section_id, item_id):
    try:
        user = request.user
        menuitem = menuItem.objects.get(pk=item_id)
        orders = Order.objects.filter(user=user.id)
        toppings = Topping.objects.all()
    except KeyError:
        pass
    context = {
        'user': user,
        'menuitem': menuitem,
         "orders": orders,
        "toppings": toppings,
    }
    return render(request, "orders/create.html", context)

@login_required(login_url='/login')
def add(request):
    try:
        user = request.user
        Orders = user.orders.all()
        item_id = request.POST['itemid']
        menuitem = menuItem.objects.get(pk=item_id)
        item = menuitem.item.name
        section_id = menuitem.section.id
        menu_id = menuitem.section.menu.id
    except KeyError:
        pass
    if menuitem.item.hasToppings:
        new = Order.objects.create(user=user, menuItem=menuitem, count=1)
        has = 'True'
    else:
        has = 'False'
    context = {
        'menuitem': item,
        'hasTopping': has,
        'orders': Orders,
        'sectionid': section_id,
        'menuid': menu_id,
    } 
    return HttpResponse(JsonResponse(context))

# Edit Order page
@login_required(login_url='/login')
def edit(request, menu_id, section_id, order_id):
    try:
        user = request.user
        #orderid = int(request.POST["orderid"])
        order = Order.objects.get(pk=order_id)
        alltoppings = Topping.objects.all()
        selectedToppings = order.toppings.all()
    except KeyError:
        pass
    context = {
        "user": user,
        "order": order,
        "toppings": alltoppings,
        "selectedToppings": selectedToppings,
    }
    return render(request, "orders/edit.html", context)

@login_required(login_url='/login')
def update(request):
    return HttpResponse({'hello':'hello'})


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
    return HttpResponseRedirect(reverse("delete", args=(menu_id,section_id,)))
