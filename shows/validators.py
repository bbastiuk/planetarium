from rest_framework.exceptions import ValidationError
from .models import Ticket

def validate_seat_is_available(show_session, row, seat):
    if Ticket.objects.filter(show_session=show_session, row=row, seat=seat).exists():
        raise ValidationError(f"Seat {row}-{seat} is already taken for this session.")

    dome = show_session.cinema_hall
    if row < 1 or row > dome.rows:
        raise ValidationError(f"Row {row} is out of bounds. This dome has {dome.rows} rows.")

    if seat < 1 or seat > dome.seats_in_row:
        raise ValidationError(f"Seat {seat} is out of bounds. Each row has {dome.seats_in_row} seats.")
