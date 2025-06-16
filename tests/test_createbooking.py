import allure
import pytest
import requests
import jsonschema
from schemas.CreateBookingSchema import CREATEBOOKING_SCHEMA

@allure.feature("Test Create Booking")
@allure.story('Creating booking')
def test_create_booking(api_client, generate_random_booking_data):
    with allure.step("Preparing data for request"):
        json = generate_random_booking_data
    with allure.step("Creating booking"):
        response = api_client.create_booking(json)
    with allure.step("Assert body"):
        assert 'bookingid' in response, 'No booking id in reponse'
        assert json['firstname'] == response['booking']['firstname'], 'First name didnt match'
        assert json['lastname'] == response['booking']['lastname'], 'Last name didnt match'
        assert json['totalprice'] == response['booking']['totalprice'], 'Total price didnt match'
        assert json['depositpaid'] == response['booking']['depositpaid'], 'Deposit paid didnt match'
        assert json['additionalneeds'] == response['booking']['additionalneeds'], 'Additional needs didnt match'
        assert json['bookingdates']['checkin'] == response['booking']['bookingdates'][
            'checkin'], 'Checkin date didnt match'
        assert json['bookingdates']['checkout'] == response['booking']['bookingdates'][
            'checkout'], 'Checkout date didnt match'

    with allure.step("Validating response body"):
        jsonschema.validate(response, CREATEBOOKING_SCHEMA)








