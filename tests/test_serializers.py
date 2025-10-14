import pytest
from shows.serializers import (
    AstronomyShowSerializer,
    ShowThemeSerializer,
    ShowSessionSerializer,
    ReservationSerializer,
    TicketSerializer,
)
from django.utils import timezone


@pytest.mark.django_db
def test_astronomy_show_serializer_required(theme):
    ser = AstronomyShowSerializer(data={"duration_minutes": 30})
    assert not ser.is_valid()
    assert "name" in ser.errors


@pytest.mark.django_db
def test_astronomy_show_serializer_write_themes(theme):
    ser = AstronomyShowSerializer(
        data={"name": "Galaxies", "duration_minutes": 60, "themes": [theme.id]}
    )
    assert ser.is_valid(), ser.errors
    obj = ser.save()
    assert obj.themes.count() == 1


@pytest.mark.django_db
def test_show_session_serializer_create(show, dome):
    payload = {
        "astronomy_show": show.id,
        "cinema_hall": dome.id,
        "start_time": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
    }
    ser = ShowSessionSerializer(data=payload)
    assert ser.is_valid(), ser.errors
    instance = ser.save()
    assert instance.astronomy_show_id == show.id
    assert instance.cinema_hall_id == dome.id


@pytest.mark.django_db
def test_ticket_serializer_requires_fields(reservation):
    ser = TicketSerializer(data={"reservation": reservation.id})
    assert not ser.is_valid()
    assert {"show_session", "row", "seat"} & set(ser.errors.keys())
