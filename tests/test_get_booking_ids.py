import allure
import pytest
from pydantic import ValidationError
from conftest import api_client
from core.models.booking_ids import BookingResponse


@allure.feature("Test Get Booking ids")
@allure.story('Getting booking all ids')
def test_get_booking_ids(api_client):
    with allure.step('Getting booking all ids'):
        response = api_client.get_booking_ids()
        response_json = response.json()
    with allure.step("Asserting status code"):
        assert response.status_code == 200, 'Status code is not 200'
    with allure.step('Asserting body response'):
        try:
            BookingResponse.model_validate(response_json)
        except ValidationError as e:
            raise ValidationError(f'Response validation error: {e}')


@allure.feature("Test Get Booking ids with name filtration")
@allure.story('Getting booking all ids with first name')
def test_get_booking_ids_name(api_client):
    with allure.step('Getting booking all ids'):
        response = api_client.get_booking_ids(params={"firstname": "lacy"})
        response_json = response.json()
    with allure.step("Asserting status code"):
        assert response.status_code == 200, 'Status code is not 200'
    with allure.step('Asserting body response'):
        try:
            BookingResponse.model_validate(response_json)
        except ValidationError as e:
            raise ValidationError(f'Response validation error: {e}')


@allure.feature("Test Get Booking ids with last name filtration")
@allure.story('Getting booking all ids with last name')
def test_get_booking_ids_lastname(api_client):
    with allure.step('Getting booking all ids'):
        response = api_client.get_booking_ids(params={"lastname": "brown"})
        response_json = response.json()
    with allure.step("Asserting status code"):
        assert response.status_code == 200, 'Status code is not 200'
    with allure.step('Asserting body response'):
        try:
            BookingResponse.model_validate(response_json)
        except ValidationError as e:
            raise ValidationError(f'Response validation error: {e}')


@allure.feature("Test Get Booking ids with name and last filtration")
@allure.story('Getting booking all ids with name and last name')
def test_get_booking_ids_nameandlastname(api_client):
    with allure.step('Getting booking all ids'):
        response = api_client.get_booking_ids(params={"firstname": "lacy", "lastname": "brown"})
        response_json = response.json()
    with allure.step("Asserting status code"):
        assert response.status_code == 200, 'Status code is not 500'
    with allure.step('Asserting body response'):
        try:
            BookingResponse.model_validate(response_json)
        except ValidationError as e:
            raise ValidationError(f'Response validation error: {e}')




@allure.feature("Test Get Booking ids with checkin and checkout filtration")
@allure.story('Getting booking all ids with checkin and checkout filtration')
def test_get_booking_ids_checkincheckout(api_client):
    with allure.step('Getting booking all ids'):
        response = api_client.get_booking_ids(params={"checkin": "2025-01-01", "checkout": "2025-12-31"})
        response_json = response.json()
    with allure.step("Asserting status code"):
        assert response.status_code == 200, 'Status code is not 200'
    with allure.step('Asserting body response'):
        try:
            BookingResponse.model_validate(response_json)
        except ValidationError as e:
            raise ValidationError(f'Response validation error: {e}')

@allure.feature("Test Get Booking ids with checkin and checkout filtration")
@allure.story('Getting booking all ids with checkin filtration')
def test_get_booking_ids_filtrationcheckin(api_client):
    with allure.step('Getting booking all ids'):
        response = api_client.get_booking_ids(params={"checkin": "2025-01-01"})
        response_json = response.json()
    with allure.step("Asserting status code"):
        assert response.status_code == 200, 'Status code is not 200'
    with allure.step('Asserting body response'):
        try:
            BookingResponse.model_validate(response_json)
        except ValidationError as e:
            raise ValidationError(f'Response validation error: {e}')

@allure.feature("Test Get Booking ids with checkin and checkout filtration")
@allure.story('Getting booking all ids with checkout filtration')
def test_get_booking_ids_withcheckoutandflitration(api_client):
    with allure.step('Getting booking all ids'):
        response = api_client.get_booking_ids(params={"checkin": "2025-01-01", "checkout": "2025-12-31"})
        response_json = response.json()
    with allure.step("Asserting status code"):
        assert response.status_code == 200, 'Status code is not 200'
    with allure.step('Asserting body response'):
        try:
            BookingResponse.model_validate(response_json)
        except ValidationError as e:
            raise ValidationError(f'Response validation error: {e}')

@allure.feature("Test Get Booking ids with checkin and checkout filtration")
@allure.story('Getting booking all ids with wrong checkout and checkin filtration')
def test_get_booking_ids_wrong_checkinandcheckout(api_client):
    with allure.step('Getting booking all ids'):
        response = api_client.get_booking_ids(params={"checkin": "asdsadsa", "checkout": "sdasda"})
    with allure.step("Asserting status code"):
        assert response.status_code == 500, 'Status code is not 500'

