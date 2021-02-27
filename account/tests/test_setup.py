from rest_framework.test import APITestCase
from django.urls import reverse

from account.serializers import *


class TestSetUp(APITestCase):

    def setUp(self):
        self.customers_list_url = reverse("customers_list")
        self.customer_create_url = reverse("customer_create")
        self.accounts_list_url = reverse("accounts_list")
        self.account_create_url = reverse("account_create")
        self.transactions_list_url = reverse("transactions_list")
        self.transactions_create_url = reverse("transaction_create")
        self.customer_names = ["Arisha Barron", "Branden Gibson", "Rhonda Church", "Georgina Hazel"]
        self.customers = []
        self.accounts = []
        self.transactions = []
        for customer_name in self.customer_names:
            obj = Customer.objects.create(name=customer_name)
            self.customers.append(obj)

        for customer in self.customers:
            obj = Account.objects.create(customer=customer)
            self.accounts.append(obj)

        obj = Transaction.objects.create(account_from=self.accounts[0], account_to=self.accounts[1], amount=200)
        self.transactions.append(obj)

        obj = Transaction.objects.create(account_from=self.accounts[2], account_to=self.accounts[3], amount=300)
        self.transactions.append(obj)

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
