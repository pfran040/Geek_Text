from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bookDetails.models import Book
from .models import List
from django.views.decorators.http import require_POST
from cart.models import Cart
#from cart.forms import AddToCartForm
from wishlist.forms import AddToCartForm

allBooks = Book.objects.all()

# function to get lists for user currently on the page.
def getLists(request):
    return List.objects.filter(user=request.user.profile).distinct()


def getBooksOfList(allMyLists, list):
    listValues = allMyLists.filter(name__contains=list.name).values('books')
    return Book.objects.filter(id__in=listValues)


# function to handle creating a new list.
@require_POST
def createList(request):
    userProfile = request.user.profile
    p = List.objects.create(name=request.POST.get('listName'), user=userProfile)
    return redirect('wishlist:wishlist-home')


# function to handle deleting a list.
@require_POST
def deleteList(request, list_id):
    List.objects.get(id=list_id).delete()
    return redirect('wishlist:wishlist-home')


# function to handle renaming a list. NOT DONE
@require_POST
def rename(request, list_id):
    List.objects.filter(id=list_id).update(name=request.POST.get('newName'))
    return redirect('wishlist:wishlist-home')


# function to add book to wishlist. May need to do error checking for when book already exists in wishlist
@require_POST
def addBook(request, list_id, book_id):
    List.objects.get(id=list_id).books.add(Book.objects.get(id=book_id))
    return redirect('wishlist:wishlist-home')

# function to add book to wishlist from book details
@require_POST
def addBookFromBookDetails(request, book_id):
    List.objects.get(id=request.POST.get('selectedList')).books.add(Book.objects.get(id=book_id))
    return redirect('wishlist:wishlist-home')

@require_POST
def deleteBook(request, list_id, book_id):
    selectedList = List.objects.get(id=list_id)
    selectedBook = Book.objects.get(id=book_id)
    selectedList.books.remove(selectedBook)
    return redirect('wishlist:wishlist-home')


# function to delete book in wishlist. To be used for moving a book to cart or a different wishlist
def deleteBookNoRedirect(list_id, book_id):
    selectedList = List.objects.get(id=list_id)
    selectedBook = Book.objects.get(id=book_id)
    selectedList.books.remove(selectedBook)


# function to move book to cart. Should delete book from its wishlist and then place it in the shopping cart of the user.
'''
@require_POST
def moveToCart(request, list_id, book_id):
    # deletes book from wishlist
    deleteBookNoRedirect(list_id, book_id)

    # adds to cart
    userCart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    form = AddToCartForm(request.POST)

    # Not sure how to do this.
    if form.is_valid():
        data = form.cleaned_data
        #userCart.add(book=book, change_amount=data['change_amount'])
        return redirect('wishlist:wishlist-home')
    else:
        return HttpResponseNotFound("moveToCart error ---- form.is_valid(): " + str(form.is_valid())
                                    + " ---- book: " + str(book) + " ---- from list: " +
                                    List.objects.get(id=list_id).name)
'''

# function to delete book from wishlist and add to shopping cart
# works if i delete the @require_POST on the cart:addToCart
@require_POST
def moveToCart(request, list_id, book_id):
    deleteBookNoRedirect(list_id, book_id)
    return redirect('cart:addToCart', book_id)

@require_POST
def moveBook(request, listFrom_id, listTo_id, book_id):
    deleteBookNoRedirect(listFrom_id, book_id)
    addBook(request, listTo_id, book_id)
    return redirect('wishlist:wishlist-home')


@login_required()
def index(request):
    # Gets all the lists associated with the user and sets it to a variable.
    myLists = getLists(request)

    # Gets the count of all the lists associated with the user.
    myListsCount = myLists.count()

    # Values for if no lists exists.
    firstList = secondList = thirdList = []
    firstBooks = secondBooks = thirdBooks = []

    if myListsCount > 0:                #first list
        firstList = myLists[0]
        firstBooks = getBooksOfList(myLists, firstList)
        if myListsCount > 1:            #second list
            secondList = myLists[1]
            secondBooks = getBooksOfList(myLists, secondList)
            if myListsCount > 2:        #third list
                thirdList = myLists[2]
                thirdBooks = getBooksOfList(myLists, thirdList)

    return render(request, 'wishlist/index.html',
                  {'allBooks': allBooks, "myLists": myLists,
                   'myListsCount': myListsCount, 'firstList': firstList, 'firstBooks': firstBooks,
                   'secondList': secondList, 'secondBooks': secondBooks,
                   'thirdList': thirdList, 'thirdBooks': thirdBooks})
