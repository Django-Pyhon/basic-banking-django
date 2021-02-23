from django.urls import path, include
from account.views import *

urlpatterns = [
    path('api/customers/', ListCustomers.as_view()),
    path('api/customer/<int:pk>', CustomerAPI.as_view()),
    path('api/customer/', CustomerCreateAPI.as_view()),
    path('api/accounts/', ListAccounts.as_view()),
    path('api/account/<int:pk>', AccountAPI.as_view()),
    path('api/account/', AccountCreateAPI.as_view()),
    path('api/transactions/', ListTransactions.as_view()),
    path('api/transaction/<int:pk>', TransactionAPI.as_view()),
    path('api/transaction/', TransactionCreateAPI.as_view()),
]
