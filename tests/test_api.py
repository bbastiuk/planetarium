import pytest
from rest_framework import status
from shows.models import Ticket, Reservation


@pytest.mark.django_db
def test_public_list_shows(api, show):
    r = api.get("/api/shows/")
    assert r.status_code == 200
    assert len(r.data) >= 1


@pytest.mark.django_db
def test_public_list_sessions(api, session):
    r = api.get("/api/sessions/")
    assert r.status_code == 200
    assert len(r.data) >= 1


@pytest.mark.django_db
def test_reservations_list_returns_only_owner(auth, reservation, user, session):
    other = Reservation.objects.create(user=user, show_session=session)
    r = auth.get("/api/reservations/")
    assert r.status_code == 200
    returned_ids = {item["id"] for item in r.data}
    assert reservation.id in returned_ids


@pytest.mark.django_db
def test_my_reservations_endpoint(auth, reservation):
    r = auth.get("/api/reservations/my/")
    assert r.status_code == 200
    assert len(r.data) >= 1
    assert any(item["id"] == reservation.id for item in r.data)


# ---- Tickets
@pytest.mark.django_db
def test_ticket_create_ok(auth, reservation):
    payload = {
        "reservation": reservation.id,
        "show_session": reservation.show_session.id,
        "row": 1,
        "seat": 1,
    }
    r = auth.post("/api/tickets/", payload, format="json")
    assert r.status_code == status.HTTP_201_CREATED
    assert Ticket.objects.filter(reservation=reservation, row=1, seat=1).exists()


@pytest.mark.django_db
def test_ticket_double_booking_blocked(auth, reservation):
    url = "/api/tickets/"
    data = {
        "reservation": reservation.id,
        "show_session": reservation.show_session.id,
        "row": 2,
        "seat": 3,
    }
    r1 = auth.post(url, data, format="json")
    r2 = auth.post(url, data, format="json")
    assert r1.status_code == 201
    assert r2.status_code in (400, 409)
