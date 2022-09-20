import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def investment(db, user):
    return baker.make("core.Investment", owner=user)


def test_list_investments(investment):
    client = APIClient()
    client.force_authenticate(user=investment.owner)
    response = client.get(reverse("core:investment-list"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["uuid"] == str(investment.uuid)


def test_list_investments_with_another_owner(investment, other_user):
    client = APIClient()
    client.force_authenticate(user=other_user)
    response = client.get(reverse("core:investment-list"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 0
