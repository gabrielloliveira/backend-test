import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
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
        return f"{self.owner} : {self.status}"

    @property
    def expected_balance(self):
        return self.initial_value


class Gain(DefaultModel):
    investment = models.ForeignKey("core.Investment", verbose_name=_("investimento"), on_delete=models.CASCADE)
    investment_value = models.DecimalField(_("valor do investimento"), max_digits=15, decimal_places=2)
    total = models.DecimalField(_("valor do ganho"), max_digits=15, decimal_places=2)
    period = models.DateField(_("período referente"))

    class Meta:
        verbose_name = _("Ganho")
        verbose_name_plural = _("Ganhos")
