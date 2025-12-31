from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_category, name='index_category'),
    path('new/', views.new_category, name='new_category'),
    path('<int:category_id>/', views.show_category, name='show_category'),
    path('<int:category_id>/edit/', views.edit_category, name='edit_category'),
]
