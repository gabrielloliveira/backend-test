from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from model_bakery import baker


def test_investment_with_started_date_in_future(db, user):
    """Investment should not be created with started_date in future"""
    tomorrow = timezone.now().date() + timedelta(days=1)
    with pytest.raises(ValidationError) as e:
        baker.make("core.Investment", started_date=tomorrow, owner=user)


def test_investment_with_started_date_in_past_or_today(db, user):
    """Investment should be created with started_date in past or today"""
    yesterday = timezone.now().date() - timedelta(days=1)
    baker.make("core.Investment", started_date=yesterday)
    baker.make("core.Investment", started_date=timezone.now().date())
    assert True


def test_investment_with_initial_value_lt_0(db, user):
    """Investment should not be created with initial_value < 0"""
    with pytest.raises(ValidationError) as e:
        baker.make("core.Investment", owner=user, initial_value=-1)


def test_investment_with_initial_value_gte_0(db, user):
    """Investment should not be created with initial_value < 0"""
    baker.make("core.Investment", owner=user, initial_value=0)
    baker.make("core.Investment", owner=user, initial_value=50)
    assert True
