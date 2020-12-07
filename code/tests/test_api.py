import pytest
import allure
from faker import Faker
from _pytest.fixtures import FixtureRequest
from api.api_client import AppClient
from mysql_client.orm_builder import MysqlOrmBuilder


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, request: FixtureRequest):
        self.api_client: AppClient = request.getfixturevalue('api_client')
        self.db : MysqlOrmBuilder = request.getfixturevalue('db_setup')

    @pytest.fixture(scope='function', autouse=False)
    def new_user(self):
        new = self.db.add_user()
        yield new
        self.db.delete_user(new.id)

    @pytest.fixture(scope='function', autouse=False)
    def not_granted_user(self):
        new = self.db.add_user(access=False)
        yield new
        self.db.delete_user(new.id)


class TestApp(BaseCase):

    @allure.title("Проверка статуса пользователя при авторизации")
    @pytest.mark.API
    def test_auth_positive(self, new_user):
        """Sending post request to /login and checking response"""
        new = new_user
        response = self.api_client.login(new.username, new.password)
        assert new.username in response

    @allure.title("Response status for unauthorized")
    @pytest.mark.API
    def test_auth_neg(self):
        """Sending post request to /login and checking response"""
        username, password = 'new12312', '1231231231'
        response = self.api_client.login(username, password)
        assert response == 'UNAUTHORIZED'

    @pytest.mark.API
    def test_auth_access_denied(self):
        new = self.db.add_user(access=False)
        login = new.username
        passwd = new.password
        response = self.api_client.login(login, passwd)
        self.db.delete_user(new.id)
        assert response == 'UNAUTHORIZED'

    @pytest.mark.API
    def test_reg_pos(self):
        """Формируется Post запрос на /reg с валидными данными.
            Проверка появления нового пользователя в базе"""
        username = Faker().first_name() + '666'
        email = Faker().email()
        passwd = '192168'
        confirm = '192168'
        term = 'y'
        self.api_client.reg(username, email, passwd, confirm, term)
        assert self.db.user_is_present(email)

    @pytest.mark.API
    def test_reg_neg_shortusrname(self):
        """Провера регистрации с коротким username.
            Приложение должно возвращать 400"""
        username = '666'
        email = Faker().email()
        passwd = '192168'
        confirm = '192168'
        term = 'y'
        response = self.api_client.reg_val(username, email, passwd, confirm, term)
        usr = self.db.user_is_present(email)
        assert not usr and response == 'BAD REQUEST'

    @pytest.mark.API
    def test_reg_neg_pass_not_match(self):
        """Запрос на регистрацию с несовпадающими паролями"""
        username = Faker().first_name() + '666'
        email = Faker().email()
        passwd = '192'
        confirm = '192168'
        term = 'y'
        response = self.api_client.reg_val(username, email, passwd, confirm, term)
        usr = self.db.user_is_present(email)
        assert not usr and response == 'BAD REQUEST'

    @pytest.mark.API
    def test_reg_neg_pass_no_terms(self):
        """Запрос на регистрацию без указания значения terms"""
        username = Faker().first_name() + '666'
        email = Faker().email()
        passwd = '192168'
        confirm = '192168'
        term = ''
        response = self.api_client.reg_val(username, email, passwd, confirm, term)
        usr = self.db.user_is_present(email)
        assert not usr and response == 'BAD REQUEST'

    @pytest.mark.API
    def test_reg_dublicated_email(self, new_user):
        """Запрос на регистрацию с существующим в базе email.
            Проверка ответа"""
        username = Faker().first_name() + '666'
        email = new_user.email
        passwd = Faker().password()
        confirm = passwd
        term = 'y'
        response = self.api_client.reg_val(username, email, passwd, confirm, term)
        usr = self.db.user_is_present(email)
        assert usr
        assert response == 'BAD REQUEST', f"Wrong: code{response}, should be 400"

    @pytest.mark.API
    def test_is_active_afterlogout(self, new_user):
        """ Проверка на активность после logout"""
        self.api_client.login(new_user.username, new_user.password)
        current = self.db.get_user(new_user.email).active
        self.api_client.logout()
        updated = self.db.get_user(new_user.email).active
        assert current == 1 and updated == 0

    @allure.title("Проверка ответа сервера при создании аккаунта")
    @pytest.mark.API
    def test_add_user(self, new_user):
        """Добавление пользователя.
             Отправка запроса на /add_user Cheking response"""
        granted_user = new_user
        username = Faker().first_name() + '666'
        email = Faker().email()
        passwd = Faker().password()
        self.api_client.login(granted_user.username, granted_user.password)
        response = self.api_client.add_user(username, email, passwd)
        usr = self.db.user_is_present(email)
        assert usr
        assert response == 'User was added!', f"{response}"

    @pytest.mark.API
    def test_add_user_unauthorized(self):
        username = Faker().first_name() + '666'
        email = Faker().email()
        passwd = Faker().password()
        response = self.api_client.add_user(username, email, passwd)
        assert response == 'UNAUTHORIZED'

    @pytest.mark.API
    def test_add_user_already_exists(self, new_user):
        """Добавление пользователя с коротким username.
         Проверка валидации."""
        granted_user = new_user
        self.api_client.login(granted_user.username, granted_user.password)
        response = self.api_client.add_user(granted_user.username, granted_user.email, granted_user.password)
        assert response == 'AlREADY EXTISTS'

    @allure.title("Проверка создания пользователя  с невалидными данными")
    @pytest.mark.API
    def test_add_user_short_username(self, new_user):
        """Проверка создания пользователя невалидными данными.
                Запрос по урлу /api/add_user с невалидными данными пользователя, проверка данных в базе.
                Данные по пользователю в бд должны отсутствовать(пользователь не создан).
                """
        granted_user = new_user
        self.api_client.login(granted_user.username, granted_user.password)
        username = Faker().lexify(text='??')
        email = Faker().email()
        passwd = Faker().password()
        response = self.api_client.add_user(username, email, passwd)
        assert not self.db.user_is_present(email), f"Wrong: this user was added without validation. Recieved response {response}"
        assert response == 'BAD REQUEST', f"{response}"

    @allure.title("Проверка создания пользователя  с невалидными данными")
    @pytest.mark.API
    def test_add_user_long_username(self, new_user):
        """Проверка создания пользователя невалидными данными.
            Запрос по урлу /api/add_user с невалидными данными пользователя, проверка данных в базе.
            Данные по пользователю в бд должны отсутствовать(пользователь не создан).
            """
        granted_user = new_user
        self.api_client.login(granted_user.username, granted_user.password)
        username = Faker().lexify(text='?????????????????')
        email = Faker().email()
        passwd = Faker().password()
        response = self.api_client.add_user(username, email, passwd)
        assert not self.db.user_is_present(email), f"Wrong: this user is present. Recieved response {response}"
        assert response == 'BAD REQUEST', f"{response},should be 400"

    @allure.title("Проверка создания пользователя с невалидным email")
    @pytest.mark.API
    def test_add_user_invalid_email(self, new_user):
        """Проверка создания пользователя невалидным email.
            Запрос по урлу /api/add_user с невалидными данными пользователя, проверка данных в базе.
            Данные по пользователю в бд должны отсутствовать(пользователь не создан) and response 400
            """
        granted_user = new_user
        self.api_client.login(granted_user.username, granted_user.password)
        username = Faker().first_name() + '666'
        email = 'amasd.com'
        passwd = Faker().password()
        response = self.api_client.add_user(username, email, passwd)
        assert not self.db.user_is_present(email), f"Wrong: this user is present. Recieved response {response}"
        assert response == 'BAD REQUEST', f"{response},should be 400"

    @allure.title("Проверка создания пользователя  с невалидными данными")
    @pytest.mark.API
    def test_add_user_empty_password(self, new_user):
        """Добавление пользователя с пустым полем пароля.
        Проверка валидации."""
        granted_user = new_user
        self.api_client.login(granted_user.username, granted_user.password)
        username = Faker().first_name() + '666'
        email = Faker().email()
        passwd = ''
        response = self.api_client.add_user(username, email, passwd)
        assert not self.db.user_is_present(email), f"Wrong: this user was added without validation. Recieved response {response}"
        assert response == 'BAD REQUEST', f"{response}"

    @allure.title("Добавление пользователя с существующим в базе email")
    @pytest.mark.API
    def test_add_user_dublicate_email(self, new_user):
        """Добавление пользователя с существующим в базе email.
                Проверка валидации."""
        granted_user = new_user
        self.api_client.login(granted_user.username, granted_user.password)
        username = Faker().first_name() + '666'
        email = granted_user.email
        passwd = Faker().password()
        response = self.api_client.add_user(username, email, passwd)
        assert self.db.user_is_present(email)
        assert response == 'BAD REQUEST', f"{response}, should be 400"

    @pytest.mark.API
    def test_delete_user(self, new_user):
        """Удаление пользователя. Проверка на отсуствие в базе и статус ответа"""
        granted_user = new_user
        self.api_client.login(granted_user.username, granted_user.password)
        response = self.api_client.delete_user(granted_user.username)
        assert not self.db.user_is_present(granted_user.email) and response == 204

    @pytest.mark.API
    def test_delete_unauthorized(self, new_user):
        granted_user = new_user
        response = self.api_client.delete_user(granted_user.username)
        assert response == 'UNAUTHORIZED'

    @pytest.mark.API
    def test_delete_notExists(self, new_user):
        """Удаление несущевтующего пользователя. Проверка ответа """
        granted_user = new_user
        self.api_client.login(granted_user.username, granted_user.password)
        response = self.api_client.delete_user(Faker().last_name())
        assert response == 'NOT FOUND'

    @pytest.mark.API
    def test_delete_notGranted(self, new_user):
        not_granted_user = self.db.add_user(access=False)
        self.api_client.login(not_granted_user.username, not_granted_user.password)
        response = self.api_client.delete_user(not_granted_user.username)
        assert response == 'UNAUTHORIZED'

    @pytest.mark.API
    def test_block_user(self, new_user):
        granted_user = new_user
        self.api_client.login(granted_user.username, granted_user.password)
        response = self.api_client.block_user(granted_user.username)
        usr = self.db.get_user(granted_user.email)
        assert usr.access == 0 and response == 'User was blocked!'

    @pytest.mark.API
    def test_block_user_unauthorized(self, new_user):
        granted_user = new_user
        response = self.api_client.block_user(granted_user.username)
        usr = self.db.get_user(granted_user.email)
        assert usr.access == 1 and response == 'UNAUTHORIZED'

    @pytest.mark.API
    def test_block_user_already_blocked(self, new_user):
        granted_user = new_user
        self.api_client.login(granted_user.username, granted_user.password)
        not_granted_user = self.db.add_user(access=False)
        response = self.api_client.block_user(not_granted_user.username)
        usr = self.db.get_user(not_granted_user.email)
        self.db.delete_user(usr.id)
        assert usr.access == 0 and response == 'ALREADY BLOCKED'

    @pytest.mark.API
    def test_block_user_not_exists(self, new_user):
        granted_user = new_user
        self.api_client.login(granted_user.username, granted_user.password)
        response = self.api_client.block_user(Faker().last_name())
        assert response == 'NOT FOUND'

    @allure.title("Блокировка пользователя во время пребывания на странице")
    @pytest.mark.API
    def test_block_user_active_after(self, new_user):
        """Блокировка пользователя во время пребывания на странице.
                Запрос по урлу /api/block_user/<username> с именем пользователя, у каоторого active = 1.
                Пользователь блокируется и деавторизируется access = 0 active = 0.
                """
        granted_user = new_user
        self.api_client.login(granted_user.username, granted_user.password)
        before = self.db.get_user(granted_user.email).active
        response = self.api_client.block_user(granted_user.username)
        usr = self.db.get_user(granted_user.email)
        assert before == 1 and usr.active == 0 and response == 'User was blocked!', "Wrong: stayed active after blocking"

    @pytest.mark.API
    def test_accept_user(self, new_user, not_granted_user):
        granted_user = new_user
        self.api_client.login(granted_user.username, granted_user.password)
        response = self.api_client.accept_user(not_granted_user.username)
        usr = self.db.get_user(not_granted_user.email)
        assert usr.access == 1 and response == 'User access granted!'

    @pytest.mark.API
    def test_accept_user_unauthorized(self, not_granted_user):
        response = self.api_client.accept_user(not_granted_user.username)
        usr = self.db.get_user(not_granted_user.email)
        assert usr.access == 0 and response == 'UNAUTHORIZED'

    @pytest.mark.API
    def test_accept_user_already_done(self, new_user):
        granted_user = new_user
        self.api_client.login(granted_user.username, granted_user.password)
        response = self.api_client.accept_user(granted_user.username)
        usr = self.db.get_user(granted_user.email)
        assert usr.access == 1 and response == 'ALREADY ACCEPTED'

    @pytest.mark.API
    def test_status(self):
        response = self.api_client.status()
        assert response == '{"status":"ok"}\n'
