from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpRequest, JsonResponse 
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie, requires_csrf_token, csrf_protect
from django.views.decorators.vary import vary_on_headers
from django.template import RequestContext

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
def create(request, menu_id, section_id):
    try:
        user = request.user
        menuitemid = int(request.POST["menuitemid"])
        menuitem = menuItem.objects.get(pk=menuitemid)
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

# update edited order
# @login_required(login_url='/login')
# def update(request, menu_id, section_id, order_id):
#     try:
#         user = request.user
#         order = Order.objects.get(pk=order_id)
#     except KeyError:
#         pass
#     return HttpResponseRedirect(reverse("edit", args=(menu_id,section_id, order_id)))



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
    return HttpResponseRedirect(reverse("edit", args=(menu_id,section_id,)))

#A request that makes changes in the database - should use POST.
#GET should be used only for requests that do not affect the state of the system.
# @require_http_methods(["POST"])
# @csrf_exempt
# def createOrder(request):
#     if request.method == "POST":
#         data = {'result': 'Good' }
#     else:
#         data = {'result': 'shit' }
#     return JsonResponse(data)
        

    

# def post(request):
#     if request.method == "POST": #os request.GET()
#         get_value= request.body
#         # Do your logic here coz you got data in `get_value`
#         data = {}
#         data['result'] = 'you made a request'
# #         return HttpResponse(json.dumps(data), content_type="application/json")