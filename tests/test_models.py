import pytest
from django.db import IntegrityError
from shows.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket,
)
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_objects_and_relations():
    t = ShowTheme.objects.create(name="Stars")
    s = AstronomyShow.objects.create(name="Night Sky", duration_minutes=40)
    s.themes.add(t)
    d = PlanetariumDome.objects.create(name="Dome A", rows=4, seats_in_row=6)
    ss = ShowSession.objects.create(
        astronomy_show=s, cinema_hall=d, start_time=timezone.now()
    )
    u = User.objects.create_user(username="alice", password="x")
    r = Reservation.objects.create(user=u, show_session=ss)

    assert s.themes.count() == 1
    assert str(t) == "Stars"
    assert str(s) == "Night Sky"
    assert str(d) == "Dome A"
    assert "@" in str(ss)  # "Show @ 2025-..."
    assert "Reservation by" in str(r)


@pytest.mark.django_db
def test_ticket_unique_together_prevents_double_booking(session, reservation):
    Ticket.objects.create(reservation=reservation, show_session=session, row=1, seat=1)
    with pytest.raises(IntegrityError):
        Ticket.objects.create(
            reservation=reservation, show_session=session, row=1, seat=1
        )
