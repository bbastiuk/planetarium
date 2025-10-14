import pytest
from django.core.exceptions import ValidationError
from shows.models import Ticket
from shows.validators import validate_seat_is_available


@pytest.mark.django_db
def test_validate_seat_is_available_free(session):
    validate_seat_is_available(session, row=2, seat=3)


@pytest.mark.django_db
def test_validate_seat_is_available_occupied(session, reservation):
    Ticket.objects.create(reservation=reservation, show_session=session, row=2, seat=3)
    with pytest.raises(ValidationError):
        validate_seat_is_available(session, row=2, seat=3)
