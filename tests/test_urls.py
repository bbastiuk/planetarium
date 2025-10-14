import pytest


@pytest.mark.django_db
def test_router_paths_exist(api):
    assert api.get("/api/shows/").status_code in (200, 403)
    assert api.get("/api/themes/").status_code in (200, 403)
    assert api.get("/api/sessions/").status_code in (200, 403)

    assert api.get("/api/reservations/my/").status_code in (200, 401, 403)
