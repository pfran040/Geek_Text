from django.urls import path
from . import views

app_name = 'wishlist'
urlpatterns = [
    path('', views.index, name='wishlist-home'),
    path('create/', views.createList, name="createList"),
    path('deleteList/<int:list_id>', views.deleteList, name="deleteList"),
    path('rename/<int:list_id>', views.rename, name="rename"),  # NOT IMPLEMENTED YET
    path('deleteBook/<int:list_id>/<int:book_id>', views.deleteBook, name="deleteBook"),
    path('moveToCart/<int:list_id>/<int:book_id>', views.moveToCart, name="moveToCart"),    # CAN'T ADD TO CART
    path('moveBook/<int:listFrom_id>/<int:listTo_id>/<int:book_id>', views.moveBook, name="moveBook"),
    path('addBookFromBookDetails/<int:book_id>', views.addBookFromBookDetails, name="addBookFromBookDetails"),
]