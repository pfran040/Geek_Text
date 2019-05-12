from django.shortcuts import render

# RAUL: Importing the form for adding an item to the cart. Of course, every book
# should have an option for being added to the cart that should be displayed
# near its name, price, etc, so the "book details" package is the most logical place to put it
#from bookStore.cart.forms import AddToCartForm

# Books
def books(request):
    return render(request, 'books/books.html')

# Book details
def bookDetails(request):
    return render(request, 'books/bookDetails.html')


# =====================================================
# CODE AUTHOR: RAUL ESPINOSA
# Views necessary for the implementation of the add to cart functionality.
# =====================================================

# The form itself
#book_add_form = AddToCartForm()

# I can't actually do anything more here because the book information included in the
# bookDetails and books.html files are hard-coded and the books package doesn't have a Model
# for the books themselves, only for comments on the books.

# =====================================================
# RAUL'S CODE ENDS HERE
# =====================================================