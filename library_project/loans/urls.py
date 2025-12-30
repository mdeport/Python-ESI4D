from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_loans, name="index_loans"),
    path("<int:loan_id>/", views.show_loan, name="show_loan"),
    path("new/", views.new_loan, name="new_loan"),
    path("return/", views.return_loan, name="return_loan"),

]