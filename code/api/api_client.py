from urllib.parse import urljoin
import requests
import json
from requests.cookies import cookiejar_from_dict
from vk.settings import APP_URL, LOGIN_URL, REG_URL, ADD_USR, DEL_USR, API_URL, STATUS


class ResponseStatusCodeException(Exception):
    pass


class RequestErrorException(Exception):
    def __init__(self, *args):
        self.code = args[0]

    def __str__(self):
        return f'{self.code}'


class AppClient:

    def __init__(self):
        self.base_url = APP_URL

        self.session = requests.Session()
        self.csrf_token = None

    def auth(self, username, password):

        data = {
            'username': username,
            'password': password,
            'submit': 'Login'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Referer': LOGIN_URL,
                   'Origin': APP_URL,
                   }
        response = self.session.request('POST', LOGIN_URL, headers=headers, data=data, allow_redirects=False)

        if response.status_code == 302:
            location = response.headers['Location']
            response = self.session.request('GET', location)
        else:
            raise RequestErrorException(f'{response.status_code}')
        return response

    def reg(self, username, email, password, confirm, term):

        data = {
            'username': username,
            'email': email,
            'confirm': confirm,
            'term': term,
            'password': password,
            'submit': 'Register'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Referer': REG_URL,
                   'Origin': APP_URL,
                   }
        response = self.session.request('POST', REG_URL, headers=headers, data=data, allow_redirects=False)

        if response.status_code == 302:
            location = response.headers['Location']
            response = self.session.request('GET', location)
        else:
            raise RequestErrorException(f'{response.status_code}')
        return response

    def add_user(self, username, email, password):

        data = {
            'username': username,
            'email': email,
            'password': password
        }
        headers = {'Content-Type': 'application/json'}
        response = self.session.request('POST', ADD_USR, headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            return response.text
        elif response.status_code == 401:
            return 'UNAUTHORIZED'
        elif response.status_code == 304:
            return 'AlREADY EXTISTS'
        elif response.status_code == 400:
            return 'BAD REQUEST'
        else:
            return f'Something wrong: status is {response.status_code}'

    def delete_user(self, username):
        url = f'{DEL_USR}/{username}'
        response = self.session.request('GET', url)
        if response.status_code == 204:
            return response.status_code
        elif response.status_code == 401:
            return 'UNAUTHORIZED'
        elif response.status_code == 404:
            return 'NOT FOUND'
        else:
            return f'Something wrong: status is {response.status_code}'

    def block_user(self, username):
        url = f'{API_URL}/block_user/{username}'
        response = self.session.request('GET', url)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 304:
            return 'ALREADY BLOCKED'
        elif response.status_code == 401:
            return 'UNAUTHORIZED'
        elif response.status_code == 404:
            return 'NOT FOUND'
        else:
            return f'Something wrong: status is {response.status_code}'

    def accept_user(self, username):
        url = f'{API_URL}/accept_user/{username}'
        response = self.session.request('GET', url)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 304:
            return 'ALREADY ACCEPTED'
        elif response.status_code == 401:
            return 'UNAUTHORIZED'
        elif response.status_code == 404:
            return 'NOT FOUND'
        else:
            return f'Something wrong: status is {response.status_code}'

    def status(self):
        response = self.session.request('GET', STATUS)
        if response.status_code == 200:
            return response.text


    def login(self, username, password):
        try:
            response = self.auth(username, password)
            return response.text
        except RequestErrorException as e:
            code = str(e)
            if code == '401':
                return 'UNAUTHORIZED'
            else:
                return ''

    def logout(self):
        url = f'{APP_URL}/logout'
        self.session.get(url)

    def reg_val(self, username, email, password, confirm, term):
        try:
            response = self.reg(username, email, password, confirm, term)
            return response.text
        except RequestErrorException as e:
            code = str(e)
            if code == '400':
                return 'BAD REQUEST'
            else:
                return code
