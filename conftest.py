import pytest
from django.contrib.auth.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(username="test", password="test")


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="test_2", password="test")
