# =====================================================================================================
# CODE AUTHOR: RAUL ESPINOSA
# The views for the books.
# =====================================================================================================

from django.urls import path

from . import views

# Name of the app
app_name = 'bookDetails'

# The URLs
urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<slug:author_slug>/', views.book_list, name='book_list_by_author'),
    path('<str:book_name>/<slug:slug>/', views.book_info, name='book_info'),
    path('<str:book_name>/<slug:slug>/review/', views.add_review, name='add_review'),
]
