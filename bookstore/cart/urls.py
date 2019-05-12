# =====================================================
# CODE AUTHOR: RAUL ESPINOSA
# The URLs for the cart
# =====================================================

from django.urls import path

from . import views

# The name of the app being used; in this case
# it's the cart app
app_name = 'cart'

# The actual URL patterns
urlpatterns = [
    path('', views.cart_info, name='cart_info'),
    path('add/<int:book_id>/', views.addToCart, name='addToCart'),
    path('remove/<int:book_id>/', views.removeFromCart, name='removeFromCart'),
    path('addSFL/<int:book_id>/', views.addToSFL, name='addToSFL'),
    path('removeSFL/<int:book_id>/', views.removeFromSFL, name='removeFromSFL'),
    path('checkout/', views.checkout, name='checkout'),
]
