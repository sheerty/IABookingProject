import allure
import pytest
from pydantic import ValidationError
from conftest import api_client
from core.models.get_booking import BookingResponse

@allure.feature("Getting booking info by id")
@allure.story("Getting booking info by id")
def test_get_booking_by_id(api_client):
    with allure.step("Get booking info by id"):
        response = api_client.get_booking(34)
        response_json = response.json()
    with allure.step("Assert code"):
        assert response.status_code == 200, "status code should be 200"
    with allure.step("Asserting body"):
        try:
            BookingResponse(**response_json)
        except ValidationError as e:
            pytest.fail(f"Response validation error:\n{e}")

@allure.feature("Getting booking info by id")
@allure.story("Getting booking info by non existent")
def test_get_booking_by_non_existent_id(api_client):
    with allure.step("Get booking info by non existent id"):
        response = api_client.get_booking(9999)
    with allure.step("Assert code"):
        assert response.status_code == 404, "status code should be 404"

@allure.feature("Getting booking info by id")
@allure.story("Getting booking info by non valid")
def test_get_booking_by_non_valid_id(api_client):
    with allure.step("Get booking info by non valid id"):
        response = api_client.get_booking("abc")
    with allure.step("Assert code"):
        assert response.status_code == 404, "status code should be 404"



