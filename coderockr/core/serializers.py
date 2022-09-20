from rest_framework import serializers

from coderockr.core.models import Investment, Gain


class GainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gain
        exclude = ["id"]


class InvestmentSerializer(serializers.ModelSerializer):
    expected_balance = serializers.ReadOnlyField()
    balance = serializers.ReadOnlyField()
    tax = serializers.ReadOnlyField()
    total_amount = serializers.ReadOnlyField()
    gains = GainSerializer(many=True, source="gain_set")

    class Meta:
        model = Investment
        fields = [
            "uuid",
            "created_at",
            "updated_at",
            "started_date",
            "owner",
            "name",
            "status",
            "initial_value",
            "expected_balance",
            "balance",
            "tax",
            "total_amount",
            "gains",
        ]
