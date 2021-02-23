from .models import *
from rest_framework import serializers


class TransactionSerializer(serializers.ModelSerializer):
    account_from = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    account_to = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())

    class Meta:
        model = Transaction
        exclude = ['created_at', 'updated_at']


class AccountSerializer(serializers.ModelSerializer):
    transactions_from = TransactionSerializer(many=True, read_only=True)
    transactions_to = TransactionSerializer(many=True, read_only=True)
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = Account
        exclude = ['created_at', 'updated_at']


class CustomerSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        exclude = ['created_at', 'updated_at']
