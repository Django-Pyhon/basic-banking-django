from django.db import models

# Create your models here.
from django.utils.translation import ugettext_lazy as _


class Customer(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.name)


class Account(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    deposit = models.PositiveIntegerField(_("Deposit"), default=500)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.customer.name) if self.customer else _("Customer not found")


class Transaction(models.Model):
    account_from = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='account_from')
    account_to = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name='account_to')
    amount = models.PositiveIntegerField(_("Amount"))
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        account_from = self.account_from
        account_to = self.account_to
        account_from.deposit -= self.amount
        account_to.deposit += self.amount
        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.account_from) + ' -> ' + str(self.account_to) + ' | ' + str(self.amount)
