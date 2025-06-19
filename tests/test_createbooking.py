import allure
import pytest
from pydantic import ValidationError
from conftest import api_client
from core.models.booking import BookingResponse


@allure.feature("Test Create Booking")
@allure.story('Creating booking with custom data')
def test_create_booking(api_client):
    booking_data = {
        "firstname": "Dome",
        "lastname": "Downie",
        "totalprice": 123,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2015-02-23",
            "checkout": "2015-10-23"
        },
        "additionalneeds": "Dicks"
    }

    response = api_client.create_booking(booking_data)
    response_json = response.json()

    try:
        BookingResponse(**response_json)
    except ValidationError as e:
        raise ValidationError(f'Response validation error: {e}')

    assert response_json['booking']['firstname'] == booking_data['firstname']
    assert response_json['booking']['lastname'] == booking_data['lastname']
    assert response_json['booking']['totalprice'] == booking_data['totalprice']
    assert response_json['booking']['depositpaid'] == booking_data['depositpaid']
    assert response_json['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response_json['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert response_json['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.feature("Test Create Booking")
@allure.story('Creating booking with random data')
def test_create_booking_random_data(api_client, generate_random_booking_data):
    data = generate_random_booking_data

    response = api_client.create_booking(data)
    response_json = response.json()

    try:
        BookingResponse(**response_json)
    except ValidationError as e:
        raise ValidationError(f'Response validation error: {e}')

    assert response.status_code == 200, f'Exepected 200 got {response.status_code}'

    assert response_json['booking']['firstname'] == data['firstname']
    assert response_json['booking']['lastname'] == data['lastname']
    assert response_json['booking']['totalprice'] == data['totalprice']
    assert response_json['booking']['depositpaid'] == data['depositpaid']
    assert response_json['booking']['bookingdates']['checkin'] == data['bookingdates']['checkin']
    assert response_json['booking']['bookingdates']['checkout'] == data['bookingdates']['checkout']
    assert response_json['booking']['additionalneeds'] == data['additionalneeds']


@allure.feature("Test Create Booking")
@allure.story('Creating booking with empty json')
def test_create_booking_empty_json(api_client):
    booking_data = {
    }
    response = api_client.create_booking(booking_data)

    assert response.status_code == 500, f'Exepected 500 got {response.status_code}'


@allure.feature("Test Create Booking")
@allure.story('Creating booking with required fields only')
def test_create_booking_required_fileds_only(api_client):
    booking_data = {
        "firstname": "Doeme",
        "lastname": "Downeie",
        "totalprice": 1233,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2015-02-23",
            "checkout": "2015-10-23"
        }
    }

    response = api_client.create_booking(booking_data)
    response_json = response.json()

    try:
        BookingResponse(**response_json)
    except ValidationError as e:
        raise ValidationError(f'Response validation error: {e}')

    assert response.status_code == 200, f'Exepected 200 got {response.status_code}'

    assert response_json['booking']['firstname'] == booking_data['firstname']
    assert response_json['booking']['lastname'] == booking_data['lastname']
    assert response_json['booking']['totalprice'] == booking_data['totalprice']
    assert response_json['booking']['depositpaid'] == booking_data['depositpaid']
    assert response_json['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response_json['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']


@pytest.mark.parametrize("missing_field", ["firstname",
                                           "lastname",
                                           "totalprice",
                                           "depositpaid",
                                           "bookingdates"])
@allure.feature("Test Create Booking")
@allure.story('Creating booking with missing required fields')
def test_create_booking_missing_required_fields(api_client, missing_field):
    booking_data = {
        "firstname": "Doeme",
        "lastname": "Downeie",
        "totalprice": 1233,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2015-02-23",
            "checkout": "2015-10-23"
        }
    }

    data = booking_data

    if missing_field == "bookingdates":
        del data['bookingdates']
    else:
        data.pop(missing_field)

    response = api_client.create_booking(data)

    assert response.status_code == 500, f'Exepected 500 got {response.status_code}'


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
@allure.feature("Test Create Booking")
@allure.story('Creating booking with missing required fields')
def test_create_booking_missing_required_fields(api_client, field, value, expected_status):
    booking_data = {
        "firstname": "Doeme",
        "lastname": "Downeie",
        "totalprice": 1233,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2015-02-23",
            "checkout": "2015-10-23"
        }
    }

    data = booking_data

    if field == "bookingdates" and value is None:
        data.pop("bookingdates")
    else:
        data[field] = value

    response = api_client.create_booking(data)

    assert response.status_code == expected_status, f'Exepected {expected_status} got {response.status_code}'
