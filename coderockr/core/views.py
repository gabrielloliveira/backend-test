from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from coderockr.core.models import Investment
from coderockr.core.serializers import InvestmentSerializer


class InvestmentViewSet(ModelViewSet):
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"

    def get_queryset(self):
        return Investment.objects.filter(owner=self.request.user).order_by("-pk")

    def create(self, request, *args, **kwargs):
        request.data["owner"] = request.user.pk
        return super(InvestmentViewSet, self).create(request, *args, **kwargs)
