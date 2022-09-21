import uuid
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from coderockr.core.validators import validate_started_date


class DefaultModel(models.Model):
    created_at = models.DateTimeField(_("criado em"), auto_now_add=True)
    updated_at = models.DateTimeField(_("atualizado em"), auto_now=True)
    uuid = models.UUIDField(_("UUID"), default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Investment(DefaultModel):
    STATUS_WITHDRAW = "withdraw"
    STATUS_NOT_SETTLED = "not_settled"
    STATUS_CHOICES = (
        (STATUS_WITHDRAW, _("Retirado")),
        (STATUS_NOT_SETTLED, _("Não Liquidado")),
    )

    started_date = models.DateField(_("iniciado em"), validators=[validate_started_date])
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("dono do investimento"),
    )
    name = models.CharField(_("nome"), max_length=50, blank=True, null=True)
    status = models.CharField(_("status"), choices=STATUS_CHOICES, default=STATUS_NOT_SETTLED, max_length=11)
    initial_value = models.DecimalField(
        _("valor inicial"),
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    balance = models.DecimalField(_("balanço"), max_digits=15, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(_("taxa"), max_digits=15, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(_("Valor recebíveis"), max_digits=15, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = _("Investimento")
        verbose_name_plural = _("Investimentos")

    def __str__(self):
        return f"{self.owner} | {self.name} | {self.status}"

    def save(self, *args, **kwargs):
        if not self.balance:
            self.balance = self.initial_value
        return super(Investment, self).save(*args, **kwargs)

    @property
    def expected_balance(self):
        return Decimal(self.initial_value + self.total_gains)

    @property
    def total_gains(self):
        return sum(list(self.gain_set.values_list("total", flat=True)))

    @property
    def tax_rate(self):
        one_year_ago = timezone.now().date() - relativedelta(years=1)
        two_year_ago = timezone.now().date() - relativedelta(years=2)
        if one_year_ago <= self.started_date:
            return 22.5
        elif two_year_ago <= self.started_date:
            return 18.5
        return 15

    def sell(self):
        if self.status == self.STATUS_WITHDRAW:
            raise Exception("Investment already been sold")
        self.status = self.STATUS_WITHDRAW
        self.balance = self.expected_balance
        self.tax = (self.total_gains * Decimal(self.tax_rate)) / 100
        self.total_amount = self.balance - self.tax

        self.tax = Decimal(f"{self.tax:.2f}")
        self.total_amount = Decimal(f"{self.total_amount:.2f}")

        self.save()


class Gain(DefaultModel):
    investment = models.ForeignKey("core.Investment", verbose_name=_("investimento"), on_delete=models.CASCADE)
    investment_value = models.DecimalField(_("valor do investimento"), max_digits=15, decimal_places=2)
    total = models.DecimalField(_("valor do ganho"), max_digits=15, decimal_places=2)
    period = models.DateField(_("período referente"))

    class Meta:
        verbose_name = _("Ganho")
        verbose_name_plural = _("Ganhos")

    def __str__(self):
        return f"{self.total} | {self.investment}"

    def calculate_gain(self):
        gain = (self.investment_value * Decimal(0.52)) / 100
        return Decimal(f"{gain:.2f}")

    def save(self, *args, **kwargs):
        if not self.total:
            self.total = self.calculate_gain()
        return super(Gain, self).save(*args, **kwargs)
