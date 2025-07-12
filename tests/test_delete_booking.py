

import allure
import pytest
from pydantic import ValidationError
from conftest import api_client, create_booking


@allure.feature("Test Delete Booking")
@allure.story("Deleting Booking")
def test_delete_booking(api_client, create_booking):
    with allure.step('Deleting Booking'):
        response = api_client.delete_booking_by_id(create_booking)
    with allure.step("Asserting Status code"):
        assert response.status_code == 201, "Status code should be 201"

@allure.feature("Test Delete Booking")
@allure.story("Deleting Booking")
def test_delete_booking_by_non_existent(api_client):
    with allure.step('Deleting Booking'):
        response = api_client.delete_booking_by_id(9999999)
    with allure.step("Asserting Status code"):
        assert response.status_code == 405, "Status code should be 405"
