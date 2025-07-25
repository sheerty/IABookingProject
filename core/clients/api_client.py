import requests
import os
from dotenv import load_dotenv
from core.settings.environments import Environment
import allure
from core.settings.config import Users, Timeouts
from core.clients.endpoints import Endpoints
from requests.auth import HTTPBasicAuth

load_dotenv()


class ApiClient:
    def __init__(self):
        environment_str = os.getenv('ENVIRONMENT')
        try:
            environment = Environment[environment_str]
        except KeyError:
            raise ValueError(f'Unsupported environment: {environment_str}')

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/json',
        }

    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv("TEST_BASE_URL")
        elif environment == Environment.PROD:
            return os.getenv("PROD_BASE_URL")
        else:
            raise ValueError(f"Unsupported environment value {environment}")

    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def post(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def ping(self):
        with allure.step('Ping api client'):
            url = f'{self.base_url}{Endpoints.PING_ENDPOINT.value}'
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 201,f'Expected status code 201 but got {response.status_code}'
        return response.status_code

    def auth(self):
        with allure.step('Getting authenticate'):
            url = f'{self.base_url}{Endpoints.AUTH_ENDPOINT.value}'
            payload = {"username": Users.USERNAME.value, "password": Users.PASSWORD.value}
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT.value)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200,f'Expected status code 200 but got {response.status_code}'
        token = response.json()['token']
        with allure.step('Updating header with Authorization'):
            self.session.headers.update({'Authorization': f'Bearer {token}'})

    def get_booking_ids(self, params=None):
        with allure.step('Getting booking ids'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}'
            response = self.session.get(url, params=params)
        return response

    def delete_booking_by_id(self, booking_id):
        with allure.step('Deleting booking by id'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}'
            response = self.session.delete(url, auth=HTTPBasicAuth(Users.USERNAME.value, Users.PASSWORD.value))
        return response

    def create_booking(self, booking_data):
        with allure.step('Creating booking'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}'
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            response = self.session.post(url, json=booking_data, headers=headers)
        return response

    def get_booking(self, id):
        with allure.step('Getting booking by id'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{id}'
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            response = self.session.get(url, headers=headers)
        return response

    def update_booking(self, booking_data, booking_id):
        with allure.step('Updating booking'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}'
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            response = self.session.put(url, auth=HTTPBasicAuth(Users.USERNAME.value, Users.PASSWORD.value), json=booking_data, headers=headers)
        return response

    def partial_update_booking(self, booking_data, booking_id):
        with allure.step('Updating booking'):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}'
            response = self.session.patch(url, auth=HTTPBasicAuth(Users.USERNAME.value, Users.PASSWORD.value), json=booking_data)
            response.raise_for_status()
        with allure.step('Assert status code'):
            assert response.status_code == 200,f'Expected status code 200 but got {response.status_code}'
        return response.json()




