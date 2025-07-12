from datetime import datetime, timedelta
from faker import Faker
import pytest
from core.clients.api_client import ApiClient


@pytest.fixture(scope='session')
def api_client():
    client = ApiClient()
    client.auth()
    return client


@pytest.fixture()
def booking_dates():
    today = datetime.today()
    checkin_date = today + timedelta(days=10)
    checkout_date = checkin_date + timedelta(days=5)

    return {
        "checkin": checkin_date.strftime("%Y-%m-%d"),
        "checkout": checkout_date.strftime("%Y-%m-%d"),
    }


@pytest.fixture()
def generate_random_booking_data(booking_dates):
    faker = Faker()
    firstname = faker.first_name()
    lastname = faker.last_name()
    totalprice = faker.random_number(digits=3)
    depositpaid = faker.boolean()
    additionalneeds = faker.sentence()

    data = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "additionalneeds": additionalneeds,
        "bookingdates": booking_dates
    }
    return data


@pytest.fixture(scope='function')
def create_booking(api_client, generate_random_booking_data):
    response = api_client.create_booking(generate_random_booking_data)
    response_json = response.json()
    return response_json["bookingid"]
