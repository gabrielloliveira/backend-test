from django.contrib import admin

from coderockr.core.models import Investment, Gain


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ["owner", "initial_value", "status"]


@admin.register(Gain)
class GainAdmin(admin.ModelAdmin):
    pass
