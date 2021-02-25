from django.http import Http404
from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User, Group
from rest_framework import views, status
from rest_framework.response import Response

from account.serializers import *


class ListCustomers(views.APIView):
    def get(self, request, format=None):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


class ListAccounts(views.APIView):
    def get(self, request, format=None):
        accounts = Account.objects.select_related('customer').all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)


class ListTransactions(views.APIView):
    def get(self, request, format=None):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class CustomerAPI(views.APIView):
    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer, many=False)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(instance=customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        customer = self.get_object(pk)
        try:
            customer.delete()
            return Response("Customer delete successful!")
        except ValidationError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class CustomerCreateAPI(views.APIView):
    def post(self, request, format=None):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountAPI(views.APIView):
    def get_object(self, pk):
        try:
            return Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        account = self.get_object(pk)
        serializer = AccountSerializer(account, many=False)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        account = self.get_object(pk)
        post_data = copy.deepcopy(request.data)
        if "customer" not in post_data:
            post_data["customer"] = account.customer.id
        serializer = AccountSerializer(instance=account, data=post_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        account = self.get_object(pk)
        try:
            account.delete()
            return Response("Account delete successful!")
        except ValidationError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class AccountCreateAPI(views.APIView):
    def post(self, request, format=None):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionAPI(views.APIView):
    def get_object(self, pk):
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction, many=False)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        transaction = self.get_object(pk)
        post_data = copy.deepcopy(request.data)
        if "account_from" not in post_data:
            post_data["account_from"] = transaction.account_from.id
        if "account_to" not in post_data:
            post_data["account_to"] = transaction.account_to.id
        serializer = TransactionSerializer(instance=transaction, data=post_data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data)
            except ValidationError as e:
                return Response(e, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        transaction = self.get_object(pk)
        try:
            transaction.delete()
            return Response("Transaction delete successful!")
        except ValidationError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class TransactionCreateAPI(views.APIView):
    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data)
            except ValidationError as e:
                return Response(e, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
