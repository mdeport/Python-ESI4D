from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_author, name='index_author'),
    path('new/', views.new_author, name='new_author'),
    path('<int:author_id>/', views.show_author, name='show_author'),
]
