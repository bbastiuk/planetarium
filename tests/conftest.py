import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.utils import timezone
from shows.models import (
    AstronomyShow,
    ShowTheme,
    PlanetariumDome,
    ShowSession,
    Reservation,
)


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username="u1", password="pass1234")


@pytest.fixture
def admin_user(db):
    User = get_user_model()
    return User.objects.create_superuser(
        username="admin", email="a@ex.com", password="pass1234"
    )


@pytest.fixture
def auth(api, user):
    api.force_authenticate(user)
    return api


@pytest.fixture
def theme(db):
    return ShowTheme.objects.create(name="Cosmos")


@pytest.fixture
def show(db, theme):
    s = AstronomyShow.objects.create(
        name="Black Holes", duration_minutes=50, description="intro"
    )
    s.themes.add(theme)
    return s


@pytest.fixture
def dome(db):
    return PlanetariumDome.objects.create(name="Main Dome", rows=5, seats_in_row=8)


@pytest.fixture
def session(db, show, dome):
    return ShowSession.objects.create(
        astronomy_show=show,
        cinema_hall=dome,
        start_time=timezone.now() + timezone.timedelta(hours=1),
    )


@pytest.fixture
def reservation(db, user, session):
    return Reservation.objects.create(user=user, show_session=session)
