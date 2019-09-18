# =====================================================
# CODE AUTHOR: RAUL ESPINOSA
# The code that models the books themselves. I made this
# so that I could begin to fully implement the cart
# functionality, since at the time of writing this
# (2/9/2019) the books package does not yet have a
# functioning model for the books themselves and the
# book-related HTML catalog pages are hard-coded and thus
# cannot be used to derive info required by the cart
# (book price, name, etc)
# =====================================================

# Necessary import for working with models
from django.db import models

# For use with the get_absolute_url methods
from django.urls import reverse
from users.models import Profile
from django.core.validators import MinValueValidator, MaxValueValidator

# This class models book authors, which have a many-to-many relationship
# with books: a book can have multiple authors and authors can write multiple
# books

class Author(models.Model):
    # The author's name. Since this is only a single author,
    # their name probably won't be longer than 70 characters
    author_name = models.CharField(max_length=70)

    # The author models' slug - will be used for URLs when searching
    # for books by author.
    # The unique field allows us to index it on a DB.
    slug = models.SlugField(max_length=150, unique=True)

    # Meta class used to define the order the authors will
    # appear in
    class Meta:
        ordering = ('author_name',)

        # How we'll refer to a single author
        # in the views.py for bookDetails
        verbose_name = 'author'
        # How we'll refer to multiple authors
        # in the views.py for bookDetails
        verbose_name_plural = 'authors'

    # Saw this used in the Django docs and did some research.
    # Seems to be a Python "toString" analogue.
    def __str__(self):
        return self.author_name

    # For use when a user searches for books by author. Returns the URL.
    def get_absolute_url(self):
        return reverse('bookDetails:book_list_by_author', args=[self.slug])


# The model that represents an individual Book. I've copy-pasted
# the existing code of the makeshift
# Book class I had made in the models.py file of my cart package,
# since that had most of what I needed

class Book(models.Model):
    # The name of the book; max_length specified as
    # 100 since most book titles won't be any longer.
    # We use the db_index option to speed up database searches
    # indexed by book name
    book_name = models.CharField(max_length=80, db_index=True)

    # The book's cover. Implemented as an ImageField
    # for now, which based on the info I've seen in the
    # documentation should be the way to do it. Also
    # optional for now (null=True option),
    # so that the server won't crash
    # if there are no image files
    book_cover = models.ImageField(upload_to='books/', blank=True, null=True)

    # The book's author
    book_author = models.CharField(max_length=200)

    # The bio of the author(s); This can be lengthy, so
    # I've set the length to 1000 chars
    author_bio = models.CharField(max_length=1000)

    # Book's description. 1000 characters should suffice for this
    book_description = models.CharField(max_length=1000)

    # Book's Genre. A book might have multiple genres,
    # so 100 characters can be used
    book_genre = models.CharField(max_length=100)

    # Publishing info (publisher, release date, etc)
    # I don't know whether this should be split into
    # multiple data fields. I've combined them all into
    # 1 for simplicity's sake, at least for now
    publishing_info = models.CharField(max_length=200)

    # Average book rating, in decimal form. Only 1
    # decimal place, i.e. 4.5 or 3.4
    avg_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0, null=True, blank=True)

    # The price of each book, specified as taking 2
    # decimal places as they do in real life,
    # i.e. $15.95, not $15.95231239501...
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # A slug, according to the Django docs, is "a short label
    # for something, containing only letters, numbers, underscores
    # or hyphens", and are used in URLs. It makes them look neater.
    slug = models.SlugField(max_length=150, db_index=True)

    # Books will also be ordered by name, since no other
    # specification has been set
    class Meta:
        ordering = ('book_name',)

    # "toString" method for the Book model
    def __str__(self):
        return self.book_name

    # For use when a user searches for a book by name. Returns the URL
    def get_absolute_url(self):
        return reverse('bookDetails:book_info', args=[self.book_name, self.slug])


class Review(models.Model):
    book        = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='review')  # Each review is attached to a book
    user        = models.ForeignKey(Profile, on_delete=models.CASCADE, default="")
    display_name= models.CharField(max_length=50, default="")                               # Display name of review
    rating      = models.IntegerField(default=3, validators=[MaxValueValidator(5),
                                                             MinValueValidator(1)])         # Rating value of rating
    message     = models.CharField(max_length=150)                                          # Message body capped at 150 char
    created_on  = models.DateTimeField(auto_now_add=True)
    approved    = models.BooleanField(default=False)

    def approved(self):
        self.approved = True
        self.save()
    def __str__(self):
        return self.message
    def name(self):
        return self.display_name

#WIP, should be moved to its own app. Here for simplicity
class Purchase(models.Model):
    book            = models.ForeignKey(Book, on_delete=models.CASCADE)                    #Each purchase has a book
    User            = models.ForeignKey(Profile, on_delete=models.CASCADE)                 #Only users can purchase books
    amount          = models.IntegerField(default=1)                                       #Amount of times user purchases a specific book