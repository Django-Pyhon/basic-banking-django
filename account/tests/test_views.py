from django.urls import reverse

from .test_setup import TestSetUp
from ..models import Account


class TestViews(TestSetUp):

    def test_customers_list(self):
        res = self.client.get(self.customers_list_url)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, list)

    def test_accounts_list(self):
        res = self.client.get(self.accounts_list_url)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, list)

    def test_transactions_list(self):
        res = self.client.get(self.transactions_list_url)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, list)

    def test_customer_create_correct(self):
        for customer_name in self.customer_names:
            res = self.client.post(self.customer_create_url, data={"name": customer_name})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.data["name"], customer_name)

    def test_customer_create_false_1(self):
        for customer_name in self.customer_names:
            res = self.client.post(self.customer_create_url, data={})
            self.assertEqual(res.status_code, 400)

    def test_customer_read_correct(self):
        for customer in self.client.get(self.customers_list_url).data:
            res = self.client.get(reverse("customer_detail", kwargs={'pk': customer['id']}))
            self.assertEqual(res.status_code, 200)

    def test_customer_update_correct(self):
        for customer in self.client.get(self.customers_list_url).data:
            res = self.client.put(reverse("customer_detail", kwargs={'pk': customer['id']}),
                                  data={"name": customer["name"] + "1"})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.data["name"], customer["name"] + "1")

    def test_customer_delete_correct(self):
        for customer in self.client.get(self.customers_list_url).data:
            res = self.client.delete(reverse("customer_detail", kwargs={'pk': customer['id']}),
                                     data={})
            self.assertEqual(res.status_code, 200)

    def test_account_create_correct(self):
        for customer in self.client.get(self.customers_list_url).data:
            res = self.client.post(self.account_create_url, data={"customer": customer['id']})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.data["deposit"], 500)

    def test_account_create_false_1(self):
        for customer in self.client.get(self.customers_list_url).data:
            res = self.client.post(self.account_create_url, data={})
            self.assertEqual(res.status_code, 400)

    def test_account_read_correct(self):
        for account in self.client.get(self.accounts_list_url).data:
            res = self.client.get(reverse("account_detail", kwargs={'pk': account['id']}))
            self.assertEqual(res.status_code, 200)

    def test_account_update_correct(self):
        for account in self.client.get(self.accounts_list_url).data:
            res = self.client.put(reverse("account_detail", kwargs={'pk': account['id']}),
                                  data={"deposit": account["deposit"] + 1})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.data["deposit"], account["deposit"] + 1)

    def test_account_delete_correct(self):
        for account in self.client.get(self.accounts_list_url).data:
            res = self.client.delete(reverse("account_detail", kwargs={'pk': account['id']}),
                                     data={})
            self.assertEqual(res.status_code, 200)

    def test_transaction_create_correct(self):
        transactions = [(0, 1), (1, 2)]
        for t in transactions:
            account_from = self.accounts[t[0]]
            account_to = self.accounts[t[1]]
            amount = 200
            data = {"account_from": account_from.id,
                    "account_to": account_to.id,
                    "amount": amount}
            res = self.client.post(self.transactions_create_url, data=data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.data['amount'], amount)

    def test_transaction_create_false_1(self):
        transactions = [(0, 1), (1, 2)]
        for t in transactions:
            account_from = self.accounts[t[0]]
            account_to = self.accounts[t[1]]
            amount = 200
            data = {"account_from": account_from.id,
                    "account_to": account_to.id,
                    "amount": amount}
            res = self.client.post(self.transactions_create_url, data={})
            self.assertEqual(res.status_code, 400)

    def test_transaction_create_false_2(self):
        transactions = [(0, 1), (1, 2)]
        for t in transactions:
            account_from = self.accounts[t[0]]
            account_to = self.accounts[t[0]]
            amount = 200
            data = {"account_from": account_from.id,
                    "account_to": account_to.id,
                    "amount": amount}
            res = self.client.post(self.transactions_create_url, data=data)
            self.assertEqual(res.status_code, 400)

    def test_transaction_create_false_3(self):
        transactions = [(0, 1), (1, 2)]
        for t in transactions:
            account_from = self.accounts[t[0]]
            account_to = self.accounts[t[1]]
            amount = 500
            data = {"account_from": account_from.id,
                    "account_to": account_to.id,
                    "amount": amount}
            res = self.client.post(self.transactions_create_url, data=data)
            self.assertEqual(res.status_code, 400)

    def test_transaction_read_correct(self):
        for t in self.transactions:
            res = self.client.get(reverse("transaction_detail", kwargs={'pk': t.id}))
            self.assertEqual(res.status_code, 200)

    def test_transaction_update_correct(self):
        for t in self.transactions:
            amount = 123
            data = {"amount": amount}
            res = self.client.put(reverse("transaction_detail", kwargs={'pk': t.id}), data=data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.data['amount'], amount)

    def test_transaction_update_false(self):
        for t in self.transactions:
            amount = 1000
            data = {"amount": amount}
            res = self.client.put(reverse("transaction_detail", kwargs={'pk': t.id}), data=data)
            self.assertEqual(res.status_code, 400)

    def test_transaction_delete_correct(self):
        for t in self.transactions:
            res = self.client.delete(reverse("transaction_detail", kwargs={'pk': t.id}))
            self.assertEqual(res.status_code, 200)
