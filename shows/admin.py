from django.contrib import admin
from .models import (
    AstronomyShow, ShowTheme, ShowSession,
    PlanetariumDome, Reservation, Ticket
)


@admin.register(AstronomyShow)
class AstronomyShowAdmin(admin.ModelAdmin):
    list_display = ("name", "duration_minutes")
    list_filter = ("themes",)
    search_fields = ("name",)


@admin.register(ShowTheme)
class ShowThemeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ShowSession)
class ShowSessionAdmin(admin.ModelAdmin):
    list_display = ("astronomy_show", "cinema_hall", "start_time")
    list_filter = ("cinema_hall", "start_time")


@admin.register(PlanetariumDome)
class PlanetariumDomeAdmin(admin.ModelAdmin):
    list_display = ("name", "rows", "seats_in_row")


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("user", "show_session", "created_at")
    inlines = [TicketInline]
    list_filter = ("created_at",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("reservation", "show_session", "row", "seat")
    list_filter = ("show_session", "row")
