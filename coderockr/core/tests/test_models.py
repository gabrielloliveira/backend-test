from datetime import timedelta

import pytest
from dateutil.relativedelta import relativedelta
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


def test_gains_of_investments(db):
    """When create investment, then create gains if date in past"""
    two_months_ago = timezone.now().date() - relativedelta(months=2)
    investment = baker.make("core.Investment", initial_value=1, started_date=two_months_ago)
    expected_periods = [two_months_ago + relativedelta(months=1), two_months_ago + relativedelta(months=2)]

    assert investment.gain_set.count() == 2
    assert list(investment.gain_set.order_by("pk").values_list("period", flat=True)) == expected_periods
