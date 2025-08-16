from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('dashboard/', dashboard, name='dashboard'),
    path('catalog/', catalog, name='catalog'),
    path('logout/',logout, name='logout'),
    path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
    path('secret/', secret, name='secret'),
    path('return/<int:book_id>/', return_book, name='return_book'),
]