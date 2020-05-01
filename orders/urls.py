from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index")
]

# create template base.html
# when the user visits website they will see 
# main page with login or signup option --- index.html
# login takes user to login page --- login.html
# signup will take user to join page --- join.html
# logged in user will go to main --- main.html