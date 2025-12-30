from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_loans, name="loans_index"),
    path("new/", views.new_loan, name="new_loan"),
]