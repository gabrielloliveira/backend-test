from dateutil.relativedelta import relativedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from coderockr.core.models import Investment, Gain


def qtd_months_between_from_started_date(started_date):
    today = timezone.now().date()
    return (today.year - started_date.year) * 12 + (today.month - started_date.month)


@receiver(post_save, sender=Investment)
def create_gains(sender, instance, created, **kwargs):
    if not created:
        return

    qtd_months = qtd_months_between_from_started_date(instance.started_date)

    for i in range(1, qtd_months + 1):
        Gain.objects.create(
            investment=instance,
            investment_value=instance.expected_balance,
            period=instance.started_date + relativedelta(months=i),
        )
