# =====================================================================================================
# CODE AUTHOR: RAUL ESPINOSA
# The views for the books.
# =====================================================================================================

from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404

# Import the Form for adding products from the Cart package
from cart.forms import AddToCartForm
from .forms import ReviewForm
# Import the Author and Book models from this package's models.py file
from .models import Author, Book, Review, Purchase
from wishlist.models import List
from users.models import Profile
from django.db.models import Avg


# List all the books. Allows one to filter books by author name,
# which is why there's a parameter called author_slug

def book_list(request, author_slug=None):
    # We assume no author was specified at first
    author = None

    # Display all authors
    authors = Author.objects.all()

    # Display all books
    books = Book.objects.all()
    # If an author slug was passed in, filter books displayed
    # by author name
    if author_slug:
        author = get_object_or_404(Author, slug=author_slug)
        books = books.filter(book_author=author)

    # Return the HTML page
    return render(request, 'bookDetails/book/list.html', {'author': author,
                                                          'authors': authors,
                                                          'books': books})

# Display a single book at a time


def book_info(request, book_name, slug):
    # Attempt to retrieve the book requested based on the provided
    # name and slug
    book = get_object_or_404(Book, book_name=book_name, slug=slug)

    # The form for Adding a product To the Cart (Add To Cart = ATC)
    ATC_product_form = AddToCartForm()

    # WISHLIST CODE: Gets the lists that the user has.
    myLists = []
    if request.user.is_authenticated:
        myLists = getLists(request)

    # If we retrieved the book successfully, get its author
    # so we can reference their attributes in the HTML page
    if book:
        author_name = book.book_author
        author = get_object_or_404(Author, author_name=author_name)
    #if an admin deletes a review, recalculate avg, else calculate average ratings
    if Review.objects.filter(book=book).aggregate(Avg('rating')).get(
        'rating__avg') == None:
        book.avg_rating = 0.0
    else:
        book.avg_rating = Review.objects.filter(book=book).aggregate(Avg('rating')).get(
            'rating__avg')  #Get average rating of a book
    book.save()

    return render(request, 'bookDetails/book/detail.html', {'book': book,
                                                            'author': author,
                                                            'ATC_book_form': ATC_product_form,
                                                            'myLists': myLists})
#Author: Paul Franco
def add_review(request, book_name, slug):
    book = get_object_or_404(Book, book_name=book_name, slug=slug) #Obtain book info
    User = get_object_or_404(Profile, user=request.user)           #Obtain user info for comment

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            message     = form.cleaned_data['message']
            name        = request.POST.get('name_select')       #Get value of name_select from radio buttons
            rating      = request.POST.get('rating')            #Get rating from stars
            review      = form.save(commit=False)
            review.book = book                                  #Get book for which this review is being applied to
            review.user = User
            if name == "Username":                              #Check what user selected from name_select radio buttons
                review.display_name = User.user
            elif name == "Nickname":
                review.display_name = User.nick_name
                if len(review.display_name) == 0:                       #If nickname is not filled, use username
                    review.display_name = User.user
            elif name == "Anonymous":
                review.display_name = "Anonymous"
            else:
                review.display_name = request.user                      #Use username if no option is selected
            review.rating = rating
            review.save()                                       #Need to save rating to update the avg_rating of book
                                                                #Save form and then redirect back to book_info page for
                                                                #specific book
            return redirect('bookDetails:book_info', book_name=book.book_name, slug=book.slug)
    else:
        form = ReviewForm()
        return render(request, 'bookDetails/book/add_review.html', {'form':form})

# function to get lists for user currently on the page.
def getLists(request):
    return List.objects.filter(user=request.user.profile).distinct()
'''
#FIXME
def getBestSellers(request, book_name):
    bestSellers = []
    books = Book.objects.all
    purchseCount = Purchase.objects.filter(book=book_name).count()
'''