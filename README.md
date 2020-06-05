# Project 3

Web Programming with Python and JavaScript

# Menu Modeling
 
The modeling of the pizza menu was done in a way where the site owner can create any number of menus, menu sections, and items. Since items are reusable e.g. cheese, or 1 topping, I chose to create the item once and add items to menus using the menItem model, the site owner can select an Item and assign it to a section in a menu with the menuItems specific price, size and style. This approach allowed me to construct as many menus, sections, and menuItems as I want. Site owners can choose an image to go with each menu and section they create, this was done using ImageField which uploads the image to static/img folder which can then be called in the view as a regular model field to display the URL to the image.


# Registration login and logout

I used the authentication api and forms.py to generate the necessary fields to join the website and installed crispy to apply bootstrap classes to make the form more user friendly.

# Shopping Cart

The shopping cart was approached using 2 models  an order model, where the user can create as many orders as they want, and a Cart model where each user has a cart with a manytomany field. The cart was given a boolean field for the system to indicate if the cart has been ordered or is still in the users account, this allowed me to use IF statements to manipulate template views and server actions. Calculating the total cart price and each orders price was approached by creating methods in the Order and Cart models which I then used to call within the template to display the amounts. 

# Placing orders, Templating and views

I used 2 base.html templates, one for the registration and login found in the registration folder and a second for the rest of the application found under the orders folder. The main.html file shows a list of available menus, the menu.html shows the sections in the selected menu. Section.html is the main file where the user can see the menuItems, their cart and can checkout. When a user clicks on an item they go to create.html to customize the order by choosing toppings, adding extras, and selecting how many orders for the selected item, once a user checks out they are taken to checkout.html to see the success message.

# Viewing Orders for site admin

Site admin can view orders by clicking on the placed orders linked which shows in the menu only if you are a superuser. The orders.html file shows the list of all carts and the orders for each cart in a bootstrap modal when clicked on the name of the user which placed the order. 

# Personal Touch

For my personal touch I chose to setup stripe checkout. Once a user pays the checkout method is called which runs the stripe function and updates the cart status to clear out from the view and place it in the placed orders for the site admin. 