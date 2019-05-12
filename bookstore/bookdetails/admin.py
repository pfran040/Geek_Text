# ===============================================================================================
# CODE AUTHOR: RAUL ESPINOSA
# According to the Django documentation, the admin.py file is used to read metadata from
# the models used in a project to allow for easy management of content on a site. I'm not sure
# where the urls.py file of the bookStore package (the one this file is in now) is getting its
# admin site link from, but before I made this file, the bookStore package didn't have an admin.py
# file. I've created this so we can register the models that are relevant to the project, such
# as the cart, the books, authors, users, and so on.
# ===============================================================================================

from django.contrib import admin

# Importing the Author and Book models from the bookDetails package
from .models import Author, Book, Review, Purchase


# Registering the models
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # The list_display option sets which fields
    # are displayed on the changelist page of the
    # admin page
    list_display = ['author_name', 'slug']

    # The prepopulated_fields option is used to
    # specify fields whose value is automatically
    # set using other fields. Here I create a slug
    # using the name of the author
    prepopulated_fields = {'slug': ('author_name',)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # NOTE: I had to remove book_author from here because apparently, list_display
    # can't contain ManyToMany fields. That results in a SystemCheckError when trying to
    # run the server and make migrations.
    list_display = ['book_name', 'book_author', 'book_cover', 'author_bio'
                    , 'book_description', 'book_genre', 'publishing_info'
                    , 'avg_rating', 'price']

    # Creating the book's slug using the book's name
    prepopulated_fields = {'slug': ('book_name',)}

# ===============================================================================================
# RAUL'S CODE ENDS HERE
# ===============================================================================================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'display_name', 'message']

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['book', 'User', 'has_purchased']