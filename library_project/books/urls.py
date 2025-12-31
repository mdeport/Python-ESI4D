from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_book, name='index_book'),
    path('new/', views.new_book, name='new_book'),
    path('<int:book_id>/', views.show_book, name='show_book'),
    path('<int:book_id>/edit/', views.edit_book, name='edit_book'),
]
