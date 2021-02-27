from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from account.models import *


@receiver(pre_delete, sender=Transaction)
def transaction_delete(sender, instance, **kwargs):
    raise ValidationError('Transactions may not delete.')


@receiver(pre_delete, sender=Customer)
def customer_delete(sender, instance, **kwargs):
    raise ValidationError('Customers may not delete.')


@receiver(pre_delete, sender=Account)
def account_delete(sender, instance, **kwargs):
    raise ValidationError('Accounts may not delete.')


@receiver(pre_save, sender=Transaction)
def transaction_update_by_save(sender, instance, **kwargs):
    if instance.pk:
        raise ValidationError('Transactions may not update.')


@receiver(pre_save, sender=Customer)
def customer_update_by_save(sender, instance, **kwargs):
    if instance.pk:
        raise ValidationError('Customers may not update.')
