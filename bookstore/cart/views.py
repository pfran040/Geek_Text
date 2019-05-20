# =====================================================
# CODE AUTHOR: RAUL ESPINOSA
# The views for the Cart. I used the Django
# documentation to learn about views:

# https://docs.djangoproject.com/en/2.1/topics/http/views/
# https://docs.djangoproject.com/en/2.1/ref/views/

# EDIT: Don't know why, but my last push from when I was working in my branch
# didn't push either this or my forms.py file to the Development branch.
# =====================================================

from django.shortcuts import render, redirect, get_object_or_404
# We will need this for views that intend to change data; those
# require HTTP POST requests.
from django.views.decorators.http import require_POST

# This is the Book model from the bookDetails package I made.
from bookDetails.models import Book, Purchase
# These are the cart and cart forms.
from .cart import Cart
from .forms import AddToCartForm
from users.models import Profile


# This is the view that will handle adding/updating items

cartBooks = []

def addToCart(request, book_id):
    userCart = Cart(request)
    cartBooks.append(book_id)
    # Attempt to get the Book that has the
    # given id
    book = get_object_or_404(Book, id=book_id)
    # Validate the form for adding the item to the cart
    form = AddToCartForm(request.POST)

    # If the form is successfully validated, we
    # proceed with adding to/updating the book's
    # amount in the cart
    if form.is_valid():
        data = form.cleaned_data
        userCart.add(book=book,
                     amount=data['amount'],
                     change_amount=data['change_amount'])

    # Once finished, the function redirects the user to the page
    # that shows them the contents of their cart
    return redirect('cart:cart_info')

# This view will handle removing items.


def removeFromCart(request, book_id):
    userCart = Cart(request)
    cartBooks.remove(book_id)
    # Same as addToCart function
    book = get_object_or_404(Book, id=book_id)
    user = get_object_or_404(Profile, user=request.user)
    cartBooks.remove(book_id)
    # Simply remove the specified Book
    # from the cart
    userCart.remove(book)

    # Again, redirect to cart contents page
    return redirect('cart:cart_info')

# This view will handle adding items to
# the Saved For Later (SFL) list

def addToSFL(request, book_id):
    userCart = Cart(request)

    book = get_object_or_404(Book, id=book_id)

    # Add the specified book to the SFL list
    userCart.addSFL(book)

    return redirect('cart:cart_info')

# This view will handle adding items back
# the cart from the SFL List. Note that removing
# an item from the SFL list is equivalent to removing
# an item from the cart, so we can just use the regular
# remove function for that


def removeFromSFL(request, book_id):
    userCart = Cart(request)

    book = get_object_or_404(Book, id=book_id)

    # Remove the specified book from the SFL
    # list by putting it back in the cart
    userCart.removeSFL(book)

    return redirect('cart:cart_info')

# This view displays the cart and its contents

def cart_info(request):
    userCart = Cart(request)

    # Iterates through the cart and creates a form allowing for
    # the modification of the amount of books in the cart
    for current in userCart:
        current['update_amount_form'] = AddToCartForm(
            initial={'amount': current['amount'],
                     'change_amount': True}
        )

    return render(request, 'cart/info.html', {'userCart': userCart})


# This view displays the checkout page

def checkout(request):
    userCart = Cart(request)
    User = get_object_or_404(Profile, user=request.user)
    for i in range(len(cartBooks)):
        book = get_object_or_404(Book, id=cartBooks[i])
        Purchase.objects.create(book=book, User=User)
    # Remove all books from the cart
    userCart.clear()
    cartBooks.clear()

    return render(request, 'cart/checkout.html', {'userCart': userCart})
