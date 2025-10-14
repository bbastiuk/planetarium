import pytest
from rest_framework import status
from shows.models import Reservation


@pytest.mark.django_db
def test_anonymous_cannot_create_reservation(api, session):
    resp = api.post("/api/reservations/", {"show_session": session.id}, format="json")
    assert resp.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


@pytest.mark.django_db
def test_user_can_create_own_reservation(auth, session):
    resp = auth.post("/api/reservations/", {"show_session": session.id}, format="json")
    assert resp.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_owner_only_update_reservation(auth, reservation, user, admin_user, api):
    api.force_authenticate(admin_user)
    url = f"/api/reservations/{reservation.id}/"
    r = api.patch(url, {"show_session": reservation.show_session.id}, format="json")
    assert r.status_code in (status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND)
