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
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie, requires_csrf_token
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
        menu = Menu.objects.get(pk=menu_id)
        section = Section.objects.get(pk=section_id)
        menuitemname = section.get_menuitemname() # dont need
        items = set(menuitemname).intersection(Item.objects.all()) # dont need
        menuitems = section.menuitems.all().order_by('item', 'size')
    except Section.DoesNotExist:
        raise Http404("Section does not exist")
    context = {
        "menu": menu,
        "section": section,
        "items": items,
        "menuitems": menuitems,
    }
    return render(request, "orders/section.html", context)

#A request that makes changes in the database - should use POST.
#GET should be used only for requests that do not affect the state of the system.
@require_http_methods(["POST"])
@vary_on_headers('X_REQUESTED_WITH')
@csrf_exempt
def createOrder(HttpRequest):
    if HttpRequest.is_ajax():
        data = {'result': 'Good' }
    else:
        data = {'result': 'shit' }
    return JsonResponse(data)
        

    

