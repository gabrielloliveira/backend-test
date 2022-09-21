from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from coderockr.core.exceptions import InvestmentAlreadySold
from coderockr.core.models import Investment
from coderockr.core.serializers import InvestmentSerializer


class InvestmentViewSet(ModelViewSet):
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "uuid"

    def get_queryset(self):
        return Investment.objects.filter(owner=self.request.user).order_by("-pk")

    def get_object(self):
        return get_object_or_404(Investment, uuid=self.kwargs.get("uuid"), owner=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data["owner"] = request.user.pk
        return super(InvestmentViewSet, self).create(request, *args, **kwargs)

    @action(methods=["POST"], detail=True, url_name="sell", url_path="sell")
    def sell(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.sell()
        except InvestmentAlreadySold as e:
            return Response({"message": "Investment already been sold"}, status=status.HTTP_400_BAD_REQUEST)
        return super(InvestmentViewSet, self).retrieve(request, *args, **kwargs)
