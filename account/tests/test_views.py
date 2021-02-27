from decimal import Decimal

from django.urls import reverse

from .test_setup import TestSetUp
from ..models import Account


class TestViews(TestSetUp):

    def test_customers_list_post(self):
        res = self.client.post(self.customers_list_url)
        self.assertEqual(res.status_code, 405)

    def test_customers_list_get(self):
        res = self.client.get(self.customers_list_url)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, list)

    def test_customers_list_put(self):
        res = self.client.put(self.customers_list_url)
        self.assertEqual(res.status_code, 405)

    def test_customers_list_delete(self):
        res = self.client.delete(self.customers_list_url)
        self.assertEqual(res.status_code, 405)

    def test_accounts_list_post(self):
        res = self.client.post(self.accounts_list_url)
        self.assertEqual(res.status_code, 405)

    def test_accounts_list_get(self):
        res = self.client.get(self.accounts_list_url)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, list)

    def test_accounts_list_put(self):
        res = self.client.put(self.accounts_list_url)
        self.assertEqual(res.status_code, 405)

    def test_accounts_list_delete(self):
        res = self.client.delete(self.accounts_list_url)
        self.assertEqual(res.status_code, 405)

    def test_transactions_list_post(self):
        res = self.client.post(self.transactions_list_url)
        self.assertEqual(res.status_code, 405)

    def test_transactions_list_get(self):
        res = self.client.get(self.transactions_list_url)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, list)

    def test_transactions_list_put(self):
        res = self.client.put(self.transactions_list_url)
        self.assertEqual(res.status_code, 405)

    def test_transactions_list_delete(self):
        res = self.client.delete(self.transactions_list_url)
        self.assertEqual(res.status_code, 405)

    def test_customer_post(self):
        for customer_name in self.customer_names:
            res = self.client.post(self.customer_create_url, data={"name": customer_name})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.data["name"], customer_name)

    def test_customer_post_2(self):
        for customer_name in self.customer_names:
            res = self.client.post(self.customer_create_url, data={})
            self.assertEqual(res.status_code, 400)

    def test_customer_get(self):
        for customer in self.client.get(self.customers_list_url).data:
            res = self.client.get(reverse("customer_detail", kwargs={'pk': customer['id']}))
            self.assertEqual(res.status_code, 200)

    def test_customer_put(self):
        for customer in self.client.get(self.customers_list_url).data:
            res = self.client.put(reverse("customer_detail", kwargs={'pk': customer['id']}))
            self.assertEqual(res.status_code, 405)

    def test_customer_delete(self):
        for customer in self.client.get(self.customers_list_url).data:
            res = self.client.delete(reverse("customer_detail", kwargs={'pk': customer['id']}))
            self.assertEqual(res.status_code, 405)

    def test_account_post(self):
        for customer in self.client.get(self.customers_list_url).data:
            res = self.client.post(self.account_create_url, data={"customer": customer['id']})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.data["deposit"], '500.00')

    def test_account_post_2(self):
        for customer in self.client.get(self.customers_list_url).data:
            res = self.client.post(self.account_create_url, data={})
            self.assertEqual(res.status_code, 400)

    def test_account_get(self):
        for account in self.client.get(self.accounts_list_url).data:
            res = self.client.get(reverse("account_detail", kwargs={'pk': account['id']}))
            self.assertEqual(res.status_code, 200)

    def test_account_put(self):
        for account in self.client.get(self.accounts_list_url).data:
            res = self.client.put(reverse("account_detail", kwargs={'pk': account['id']}))
            self.assertEqual(res.status_code, 405)

    def test_account_delete(self):
        for account in self.client.get(self.accounts_list_url).data:
            res = self.client.delete(reverse("account_detail", kwargs={'pk': account['id']}))
            self.assertEqual(res.status_code, 405)

    def test_transaction_post(self):
        transactions = [(0, 1), (1, 2)]
        for t in transactions:
            account_from = self.accounts[t[0]]
            account_to = self.accounts[t[1]]
            amount = '200.00'
            data = {"account_from": account_from.id,
                    "account_to": account_to.id,
                    "amount": amount}
            res = self.client.post(self.transactions_create_url, data=data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.data['amount'], amount)

    def test_transaction_post_2(self):
        transactions = [(0, 1), (1, 2)]
        for t in transactions:
            res = self.client.post(self.transactions_create_url, data={})
            self.assertEqual(res.status_code, 400)

    def test_transaction_post_3(self):
        transactions = [(0, 1), (1, 2)]
        for t in transactions:
            account_from = self.accounts[t[0]]
            account_to = self.accounts[t[0]]
            amount = '200.00'
            data = {"account_from": account_from.id,
                    "account_to": account_to.id,
                    "amount": amount}
            res = self.client.post(self.transactions_create_url, data=data)
            self.assertEqual(res.status_code, 400)

    def test_transaction_post_4(self):
        transactions = [(0, 1), (1, 2)]
        for t in transactions:
            account_from = self.accounts[t[0]]
            account_to = self.accounts[t[1]]
            amount = '700.01'
            data = {"account_from": account_from.id,
                    "account_to": account_to.id,
                    "amount": amount}
            res = self.client.post(self.transactions_create_url, data=data)
            self.assertEqual(res.status_code, 400)

    def test_transaction_get(self):
        for t in self.transactions:
            res = self.client.get(reverse("transaction_detail", kwargs={'pk': t.id}))
            self.assertEqual(res.status_code, 200)

    def test_transaction_put(self):
        for t in self.transactions:
            res = self.client.put(reverse("transaction_detail", kwargs={'pk': t.id}))
            self.assertEqual(res.status_code, 405)

    def test_transaction_delete(self):
        for t in self.transactions:
            res = self.client.delete(reverse("transaction_detail", kwargs={'pk': t.id}))
            self.assertEqual(res.status_code, 405)
