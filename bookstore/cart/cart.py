# ====================================================================
# CODE AUTHOR: RAUL ESPINOSA
# This is the code for the actual cart functionality. A small note:
# I can't actually make the cart "work" until the models of the things
# that are supposed to go in the cart (i.e. the books) exist and can
# be imported/referenced. That being the case, I'm going to use some
# placeholder code to model the functionality needed. These can be
# refactored to the genuine book model code when it's available

# Note that I used the following resources to learn
# about django session functions and such:
# https://docs.djangoproject.com/en/2.0/topics/http/sessions/
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Sessions
# ====================================================================

# This data type simplifies floating-point arithmetic and makes it
# look more like what calculators make it look like in real life.
# Also allows for rounding rules to be established,
# which will help with price calculations
from decimal import Decimal

from django.conf import settings

# Importing my Book class from the bookDetails package I made
from bookDetails.models import Book, Purchase


# This is the cart class.
class Cart(object):
    # Constructor method for the class - includes a request parameter
    def __init__(self, request):
        # Start by creating a session for the new cart
        self.session = request.session
        # This structure is better than the try/except I had before.
        # Just try to get the cart from the current session
        userCart = self.session.get(settings.CART_SESSION_ID)

        if not userCart:
            # If we can't, just make a blank cart
            userCart = self.session[settings.CART_SESSION_ID] = {}
        # Assign the newly created and ID'd userCart to this cart model
        self.userCart = userCart

    # Our cart's status has to be modifiable, i.e. we need to be able
    # to change the state of the cart dynamically. For this, we need
    # a save function
    def save(self):
        self.session.modified = True

    # The function that will be used to add items to the cart.
    def add(self, book, amount=1, change_amount=False):
        # Get the book's ID (its Primary Key)
        book_id = str(book.id)
        # If the book isn't in the cart, add it (and all the requisite parameters
        # the cart has to show), as well as a parameter indicating whether
        # an item is saved for later (SFL) or not, which defaults to false
        if book_id not in self.userCart:
            self.userCart[book_id] = {'amount': 0,
                                      'author': book.book_author,
                                      'author_bio': book.author_bio,
                                      'description': book.book_description,
                                      'genre': book.book_genre,
                                      'publishing_info': book.publishing_info,
                                      'avg_rating': str(book.avg_rating),
                                      'price': str(book.price),
                                      'SFL': False}
        # If change_amount is True, we change the number of the specified
        # book in the cart to the specified amount
        if change_amount:
            self.userCart[book_id]['amount'] = amount

        # Otherwise, we just add the specified amount of the specified book
        # to the cart
        else:
            self.userCart[book_id]['amount'] += amount

        # Save the state of the cart, cementing our changes
        self.save()

    # Function for removing books from the cart
    def remove(self, book):
        # Same idea as in the add() function - now uses
        # book's ID!
        book_id = str(book.id)
        # If the book is in the cart, remove it,
        # then save the state of the cart
        if book_id in self.userCart:
            del self.userCart[book_id]
            self.save()

    # Function for setting a book's status as Saved For Later (SFL)
    def addSFL(self, book):
        book_id = str(book.id)

        # If the book is in the cart, set its SFL status
        # to True, indicating the book is in the saved for later
        # list
        if book_id in self.userCart:
            self.userCart[book_id]['SFL'] = True

        self.save()

    # Function for moving a book back to the cart from the
    # SFL list
    def removeSFL(self, book):
        book_id = str(book.id)

        # If the book is in the cart, set its
        # SFL status to False so that it will show up
        # in the cart again
        if book_id in self.userCart:
            self.userCart[book_id]['SFL'] = False

        self.save()

    # This iterator will be used to iterate (of course) through the
    # books in the cart, i.e. the Book models (instances)
    def __iter__(self):
        # Get the keys corresponding to all the books
        # in the database - now uses Book model's hidden ID
        # parameter!
        book_ids = self.userCart.keys()

        # Use the keys to get the actual Book objects
        # and add them to the cart
        books = Book.objects.filter(id__in=book_ids)

        # Create a copy of the current cart
        cart = self.userCart.copy()

        # Add the books to the copy of the cart
        for book in books:
            cart[str(book.id)]['book'] = book

        # Iterate over the books in the copied cart,
        # adding a price and total price attribute to each
        # item, then returning the book instance
        for book in cart.values():
            # We made the price attribute of the book a string
            # in the add method so we could serialize it (needed
            # for use w/ Sessions); now we have to convert back to
            # a Decimal value so we can perform arithmetic on it
            book['price'] = Decimal(book['price'])

            # Calculate the subtotal price for the copies of each book
            book['total_price'] = book['price'] * book['amount']

            # NOTE 2/23/19:
            # Maybe we need to add the book's other attributes here, such
            # as author name, etc...? Not sure if that's needed, since
            # we pass the book instance later
            yield book

    # Returns the total number of items in a user's cart
    def __len__(self):
        return sum(book['amount'] for book in self.userCart.values())
    # Calculates the total cost of all the books in the cart that aren't
    # listed as being saved for later
    def get_total_price(self):
        return sum((book['price'] * book['amount']) for book in self.userCart.values() if not book['SFL'])

    # Delete the cart from the session - this is functionally the same
    # as "emptying" it, since a new empty cart will be created the next time the
    # user adds a book to their cart
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
