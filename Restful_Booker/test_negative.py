import pytest
import requests
from constants import BASE_URL


class TestBookingsNegative:
    """Негативные сценарии - РЕАЛЬНЫЕ статусы Restful Booker API"""

    # POST (все возвращают 500)
    def test_post_missing_firstname(self, auth_session, invalid_missing_fields):
        response = auth_session.post(f"{BASE_URL}/booking", json=invalid_missing_fields)
        assert response.status_code == 500  # ✅

    def test_post_price_string(self, auth_session, invalid_price_string):
        response = auth_session.post(f"{BASE_URL}/booking", json=invalid_price_string)
        assert response.status_code == 500  # ✅

    def test_post_empty_data(self, auth_session, invalid_empty_data):
        response = auth_session.post(f"{BASE_URL}/booking", json=invalid_empty_data)
        assert response.status_code == 500  # ✅

    # GET
    def test_get_nonexistent_booking(self, auth_session, nonexistent_booking_id):
        response = auth_session.get(f"{BASE_URL}/booking/{nonexistent_booking_id}")
        assert response.status_code == 404  # ✅

    def test_get_invalid_id_type(self, auth_session):
        response = auth_session.get(f"{BASE_URL}/booking/invalid_id")
        assert response.status_code == 404  # ✅

    # PUT/PATCH/DELETE несуществующий (все 405)
    def test_put_nonexistent(self, auth_session, booking_data, nonexistent_booking_id):
        response = auth_session.put(f"{BASE_URL}/booking/{nonexistent_booking_id}", json=booking_data)
        assert response.status_code == 405  # ✅

    def test_patch_nonexistent(self, auth_session, patch_data, nonexistent_booking_id):
        response = auth_session.patch(f"{BASE_URL}/booking/{nonexistent_booking_id}", json=patch_data)
        assert response.status_code == 405  # ✅

    def test_delete_nonexistent(self, auth_session, nonexistent_booking_id):
        response = auth_session.delete(f"{BASE_URL}/booking/{nonexistent_booking_id}")
        assert response.status_code == 405  # ✅

    # DELETE без авторизации
    def test_delete_without_auth(self, nonexistent_booking_id):
        session = requests.Session()
        response = session.delete(f"{BASE_URL}/booking/{nonexistent_booking_id}")
        assert response.status_code == 403  # ✅ ИСПРАВЛЕНО!

    def test_post_invalid_dates(self, auth_session, invalid_booking_dates):
        """Restful Booker принимает даже некорректные даты"""
        response = auth_session.post(f"{BASE_URL}/booking", json=invalid_booking_dates)
        assert response.status_code == 200  # ✅ Реальность!
