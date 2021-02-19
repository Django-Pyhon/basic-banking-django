from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from account.models import Transaction


@receiver(pre_delete, sender=Transaction)
def transaction_delete(sender, instance, **kwargs):
    if instance.amount > instance.account_to.deposit:
        raise ValidationError(
            {'amount': _(
                'Transaction may not be undone due to insufficient balance of ') + str(
                instance.account_to)})
    instance.account_from.deposit += instance.amount
    instance.account_to.deposit -= instance.amount
    instance.account_from.save()
    instance.account_to.save()
