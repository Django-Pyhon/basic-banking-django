import copy

from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.utils.translation import ugettext_lazy as _


class Customer(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return '%d: %s' % (self.pk, self.name)


class Account(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='accounts')
    deposit = models.DecimalField(_("Deposit"), default=500.00, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return '%d: %s | %s' % (self.pk, self.customer.name, str(self.deposit))


class Transaction(models.Model):
    account_from = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions_from')
    account_to = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions_to')
    amount = models.DecimalField(_("Amount"), max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        """
        Validate the fields, then update deposits of accounts
        """
        self.validation()
        self.account_from.deposit -= self.amount
        self.account_to.deposit += self.amount
        self.account_from.save()
        self.account_to.save()
        super(Transaction, self).save(*args, **kwargs)

    def validation(self):
        errors = {}
        try:
            self.validate_accounts()
        except ValidationError as e:
            errors = e.update_error_dict(errors)

        try:
            self.validate_amount()
        except ValidationError as e:
            errors = e.update_error_dict(errors)

        try:
            self.validate_deposit()
        except ValidationError as e:
            errors = e.update_error_dict(errors)

        if errors:
            raise ValidationError(errors)

    def validate_deposit(self):
        if self.amount > self.account_from.deposit:
            raise ValidationError({'amount': _('Transaction may not more than the deposit of the account.')})

    def validate_amount(self):
        if self.amount <= 0:
            raise ValidationError({'amount': _('Transaction may not less than 0 or equal to 0.')})

    def validate_accounts(self):
        if self.account_from == self.account_to:
            raise ValidationError(_('Transaction may not be done to the same account.'))

    def __str__(self):
        return '%d: %s -> %s | %s' % (
            self.pk, self.account_from.customer.name, self.account_to.customer.name, str(self.amount))
