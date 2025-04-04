from django.conf import settings
from django.db import models


class AstronomyShow(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField()
    poster = models.ImageField(upload_to="posters/", blank=True, null=True)
    themes = models.ManyToManyField("ShowTheme", related_name="shows")

    def __str__(self):
        return self.name


class ShowTheme(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE, related_name="sessions")
    cinema_hall = models.ForeignKey(PlanetariumDome, on_delete=models.CASCADE, related_name="sessions")
    start_time = models.DateTimeField()

    def __str__(self):
        return f"{self.astronomy_show.name} @ {self.start_time}"


class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations")
    show_session = models.ForeignKey(ShowSession, on_delete=models.CASCADE, related_name="reservations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation by {self.user} for {self.show_session}"


class Ticket(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="tickets")
    show_session = models.ForeignKey(ShowSession, on_delete=models.CASCADE, related_name="tickets")
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()

    class Meta:
        unique_together = ("show_session", "row", "seat")

    def __str__(self):
        return f"Seat {self.row}-{self.seat} for {self.show_session}"
