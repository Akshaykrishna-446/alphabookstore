from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('books', views.books, name='books'),
    path('cart', views.cartlist, name='cart'),
    path('account', views.account, name='account'),
    path('order', views.order, name='orders'),
    path('signOut', views.signOut, name='signOut'),
    path('cartlist', views.cartlist, name='cartlist'),
    path('book_details/<str:book_id>', views.book_details, name='book_details'),
    path('cartremove/<id>', views.cartremove, name='cartremove'),
    path('orderremove/<id>', views.orderremove, name='orderremove'),
    
]