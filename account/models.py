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
        return str(self.name)


class Account(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    deposit = models.IntegerField(_("Deposit"), default=500)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        show = [str(self.customer.name), _("Deposit") + ': ' + str(self.deposit)]
        return ' | '.join(show)


class Transaction(models.Model):
    account_from = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name='account_from')
    account_to = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name='account_to')
    amount = models.PositiveIntegerField(_("Amount"))
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __init__(self, *args, **kwargs):
        super(Transaction, self).__init__(*args, **kwargs)
        self.old_instance_org = copy.deepcopy(self)

    def save(self, *args, **kwargs):
        self.full_clean()
        self.account_to = self.current_instance.account_to
        self.account_from = self.current_instance.account_from
        self.amount = self.current_instance.amount
        if not self._state.adding:
            if self.account_from != self.old_instance.account_from:
                self.old_instance.account_from.save()
            if self.account_to != self.old_instance.account_to:
                self.old_instance.account_to.save()
        self.account_from.save()
        self.account_to.save()
        super(Transaction, self).save(*args, **kwargs)

    def clean(self):
        self.old_instance = copy.deepcopy(self.old_instance_org)
        self.current_instance = copy.deepcopy(self)
        # Don't allow transactions to the same account
        if self.current_instance.account_from == self.current_instance.account_to:
            raise ValidationError(_('Transaction may not be done to the same account.'))
        # Don't allow transactions more than the deposit
        else:
            if not self._state.adding:
                # if accounts changes
                if self.current_instance.account_from != self.old_instance.account_from or self.current_instance.account_to != self.old_instance.account_to:
                    if self.old_instance.amount > self.old_instance.account_to.deposit:
                        raise ValidationError(
                            {'amount': _(
                                'Transaction may not be undone due to insufficient balance of ') + str(
                                self.old_instance.account_to)})
                    self.old_instance.account_from.deposit += self.old_instance.amount
                    self.old_instance.account_to.deposit -= self.old_instance.amount
                    if self.current_instance.account_from == self.old_instance.account_from:
                        self.current_instance.account_from.deposit = self.old_instance.account_from.deposit
                    if self.current_instance.account_to == self.old_instance.account_to:
                        self.current_instance.account_to.deposit = self.old_instance.account_to.deposit
                else:
                    if self.old_instance.amount > self.current_instance.account_to.deposit + self.current_instance.amount:
                        raise ValidationError(
                            {'amount': _(
                                'Transaction may not be undone due to insufficient balance of ') + str(
                                self.account_to)})
                    self.current_instance.account_from.deposit += self.old_instance.amount
                    self.current_instance.account_to.deposit -= self.old_instance.amount
            if self.current_instance.amount > self.current_instance.account_from.deposit:
                raise ValidationError(
                    {'amount': _('Transaction may not more than the deposit of the customer.')})
            self.current_instance.account_from.deposit -= self.current_instance.amount
            self.current_instance.account_to.deposit += self.current_instance.amount

    def __str__(self):
        return str(self.account_from.customer.name) + ' -> ' + str(self.account_to.customer.name) + ' | ' + str(
            self.amount)
