import allure
import pytest
from pydantic import ValidationError
from conftest import api_client, create_booking, generate_random_booking_data
from core.models.update_booking import BookingModel


@allure.feature("Update Booking")
@allure.story("Updating created booking")
def test_update_booking(api_client, create_booking, generate_random_booking_data):
    with allure.step('Preparing payload'):
        payload = generate_random_booking_data

    with allure.step('Updating booking'):
        response = api_client.update_booking(payload, create_booking)
        response_json = response.json()

    with allure.step("asserting status code"):
        assert response.status_code == 200

    with allure.step('Asserting body response'):
        try:
            BookingModel(**response_json)
        except ValidationError as e:
            raise ValidationError(f'Response validation error: {e}')

    assert response_json['firstname'] == payload['firstname']
    assert response_json['lastname'] == payload['lastname']
    assert response_json['totalprice'] == payload['totalprice']
    assert response_json['depositpaid'] == payload['depositpaid']
    assert response_json['bookingdates']['checkin'] == payload['bookingdates']['checkin']
    assert response_json['bookingdates']['checkout'] == payload['bookingdates']['checkout']
    assert response_json['additionalneeds'] == payload['additionalneeds']


@allure.feature("Update Booking")
@allure.story("Updating created booking with empty json")
def test_update_booking_emptyjson(api_client, create_booking, generate_random_booking_data):
    with allure.step('Preparing payload'):
        payload = {}

    with allure.step('Updating booking'):
        response = api_client.update_booking(payload, create_booking)

    with allure.step("asserting status code"):
        assert response.status_code == 400


@allure.feature("Update Booking")
@allure.story("Updating created booking with wrong id")
def test_update_bookingwrongid(api_client, create_booking, generate_random_booking_data):
    with allure.step('Preparing payload'):
        payload = generate_random_booking_data

    with allure.step('Updating booking'):
        response = api_client.update_booking(payload, 9999999)

    with allure.step("asserting status code"):
        assert response.status_code == 405


@pytest.mark.parametrize("missing_field", ["firstname",
                                           "lastname",
                                           "totalprice",
                                           "depositpaid",
                                           "bookingdates"])
@allure.feature("Update Booking")
@allure.story("Updating created booking with missing fields")
def test_update_booking_missingfields(api_client, create_booking, missing_field):
    with allure.step('Preparing payload'):
        payload = {
            "firstname": "Doeme",
            "lastname": "Downeie",
            "totalprice": 1233,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2015-02-23",
                "checkout": "2015-10-23"
            }
        }

    if missing_field == "bookingdates":
        del payload['bookingdates']
    else:
        payload.pop(missing_field)
    with allure.step('Updating booking'):
        response = api_client.update_booking(payload, create_booking)

    with allure.step("asserting status code"):
        assert response.status_code == 400

@pytest.mark.parametrize("field, value, expected_status", [
        # firstname
        ("firstname", True, 500),
        ("firstname", 123, 500),
        ("firstname", None, 500),

        # lastname
        ("lastname", True, 500),
        ("lastname", 456, 500),
        ("lastname", None, 500),

        # totalprice
        ("totalprice", None, 500),

        # depositpaid
        ("depositpaid", None, 500),

        # bookingdates
        ("bookingdates", None, 500),  # удаление поля
    ])
@allure.feature("Update Booking")
@allure.story("Updating created booking with  wrong values")
def test_update_booking_withwrongvalues(api_client, create_booking, field, value, expected_status):
    with allure.step('Preparing payload'):
        payload = {
        "firstname": "Doeme",
        "lastname": "Downeie",
        "totalprice": 1233,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2015-02-23",
            "checkout": "2015-10-23"
        }
    }
    with allure.step('Updating booking'):
        data = payload

        if field == "bookingdates" and value is None:
            data.pop("bookingdates")
        else:
            data[field] = value

        response = api_client.create_booking(data)

        assert response.status_code == expected_status, f'Exepected {expected_status} got {response.status_code}'