from django.urls import path, include
from account.views import *

urlpatterns = [
    path('api/customers/', ListCustomers.as_view(), name="customers_list"),
    path('api/customer/<int:pk>', CustomerAPI.as_view(), name="customer_detail"),
    path('api/customer/', CustomerCreateAPI.as_view(), name="customer_create"),
    path('api/accounts/', ListAccounts.as_view(), name="accounts_list"),
    path('api/account/<int:pk>', AccountAPI.as_view(), name="account_detail"),
    path('api/account/', AccountCreateAPI.as_view(), name="account_create"),
    path('api/transactions/', ListTransactions.as_view(), name="transactions_list"),
    path('api/transaction/<int:pk>', TransactionAPI.as_view(), name="transaction_detail"),
    path('api/transaction/', TransactionCreateAPI.as_view(), name="transaction_create"),
]
