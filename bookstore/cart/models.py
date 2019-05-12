# ====================================================================
# CODE AUTHOR: RAUL ESPINOSA
# This is the code that models a shopping cart.
# ====================================================================

from django.db import models

# The actual Cart model class.


class Cart(models.Model):
    # This tells us whether the user has checked out or not
    checkout_status = models.BooleanField(default=False)

    # This tells us the date the cart was created on... each cart
    # should have its own creation date, of course
    created_on = models.DateTimeField()


# This class models the books the site is supposed to be selling
# I've provided data fields corresponding to the requirements
# listed on the Feature Checklist, but this can and should be
# replaced by the implementation of the bookDetails that the
# corresponding team member is in charge of

class Book(models.Model):
    # The name of the book; max_length specified as
    # 100 since most book titles won't be any longer
    book_name = models.CharField(max_length=80)

    # Book's description. Max_length must be defined (wasn't giving me
    # this error before, but now it is) - I've set it to 1000 arbitrarily.
    # The other maximum parameters are also arbitrary
    book_description = models.CharField(max_length=1000)

    # Book's Genre
    book_genre = models.CharField(max_length=20)

    # Publishing info
    book_info = models.CharField(max_length=100)

    # Average book rating, in decimal form. Only 1
    # decimal place, i.e. 4.5 or 3.4
    avg_rating = models.DecimalField(max_digits=2, decimal_places=1)

    # The amount of this particular book that's in a cart
    amount = models.PositiveIntegerField()

    # The price of each book, specified as taking 2
    # decimal places as they do in real life,
    # i.e. $15.95, not $15.95231239501...
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Function that tells you how many units of a book
    # are in your cart
    def ___unicode__(self):
        return '%d copies of %s in cart' % (self.amount, self.book_name)