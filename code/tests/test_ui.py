import pytest
from _pytest.fixtures import FixtureRequest
import requests
from faker import Faker
from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage
from ui.pages.reg_page import RegPage
from ui.pages.main_page import MainPage
from vk.settings import SET_USER

class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        self.driver = driver
        self.config = config
        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.login_page: LoginPage = request.getfixturevalue('login_page')
        self.reg_page: RegPage = request.getfixturevalue('reg_page')
        self.main_page: MainPage = request.getfixturevalue('main_page')

    @pytest.fixture(scope='function', autouse=False)
    def authorize(self, db_setup):
        new = db_setup.add_user()
        self.login_page.auth_with_text(new.username, new.password)
        yield MainPage(driver=self.login_page.driver)
        db_setup.delete_user(new.id)


class Test(BaseCase):

    @pytest.mark.UI
    def test_auth(self, db_setup):
        new = db_setup.add_user()
        login = new.username
        passwd = new.password
        self.login_page.auth_with_text(login, passwd)
        is_displayed = self.login_page.login_isDisplayed(login)
        db_setup.delete_user(new.id)
        assert is_displayed

    @pytest.mark.UI
    def test_auth_neg(self):
        login = Faker().last_name() + '111'
        passwd = '192168'
        self.login_page.auth_with_text(login, passwd)
        assert self.login_page.error_isDisplayed()

    @pytest.mark.UI
    def test_reg_invalid_login_short(self):
        login = 'pepe'
        email = Faker().email()
        passwd1 = '192168'
        passwd2 = '192168'
        self.reg_page.reg_with_text(login, email, passwd1, passwd2)
        assert self.reg_page.invalid_login()

    @pytest.mark.UI
    def test_reg_invalid_login_long(self):
        login = 'pepesadasdasdasdasdasd'
        email = Faker().email()
        passwd1 = '192168'
        passwd2 = '192168'
        self.reg_page.reg_with_text(login, email, passwd1, passwd2)
        assert self.reg_page.invalid_login()

    @pytest.mark.UI
    def test_reg_invalid_email(self):
        login = Faker().last_name() + '666'
        email = 'mail@mail'
        passwd1 = '192168'
        passwd2 = '192168'
        self.reg_page.reg_with_text(login, email, passwd1, passwd2)
        assert self.reg_page.invalid_email()

    @pytest.mark.UI
    def test_reg_dublicated_email(self, db_setup):
        new = db_setup.add_user()
        login2 = Faker().first_name() + '666'
        email2 = new.email
        self.reg_page.reg_with_text(login2, email2, new.password, new.password)
        db_setup.delete_user(new.id)
        assert self.reg_page.email_exists(), "Wrong message: Internal server error, should be: email already exists"

    @pytest.mark.UI
    def test_reg_dublicated_username(self, db_setup):
        new = db_setup.add_user()
        self.reg_page.reg_with_text(new.username, new.email, new.password, new.password)
        db_setup.delete_user(new.id)
        assert self.reg_page.user_exists()

    @pytest.mark.UI
    def test_reg_passw_notmatch(self):
        login = Faker().first_name() + '666'
        email = 'mail@mail.com'
        passwd1 = '192'
        passwd2 = '192168'
        self.reg_page.reg_with_text(login, email, passwd1, passwd2)
        assert self.reg_page.pass_not_match()

    @pytest.mark.UI
    def test_reg_success(self):
        login = Faker().first_name() + '666'
        email = Faker().email()
        passwd1 = '192168'
        passwd2 = '192168'
        self.reg_page.reg_with_text(login, email, passwd1, passwd2)
        assert self.login_page.login_isDisplayed(login)

    @pytest.mark.UI
    def test_main_info_api(self, authorize):
        main_page = authorize
        redir = main_page.find_api()
        assert '/wiki/API' in redir

    @pytest.mark.UI
    def test_main_info_future(self, authorize):
        main_page = authorize
        redir = main_page.find_future()
        assert '/future-of-the-internet/' in redir

    @pytest.mark.UI
    def test_main_info_smtp(self, authorize):
        main_page = authorize
        redir = main_page.find_smtp()
        assert '/wiki/SMTP' in redir

    @pytest.mark.UI
    def test_home_button(self, authorize):
        main_page = authorize
        assert main_page.home_random_fact()

    @pytest.mark.UI
    def test_main_python_redir(self, authorize):
        main_page = authorize
        redir = main_page.python_section()
        assert 'www.python.org' in redir, f"Deviation: {redir}"

    @pytest.mark.UI
    def test_main_python_history(self, authorize):
        main_page = authorize
        redir = main_page.history_section()
        assert '/wiki/History_of_Python' in redir, f"Deviation: {redir}"

    @pytest.mark.UI
    def test_main_python_flask(self, authorize):
        main_page = authorize
        redir = main_page.flask_section()
        assert 'flask' in redir, f"Deviation: {redir}"

    @pytest.mark.UI
    def test_main_linux(self, authorize):
        main_page = authorize
        redir = main_page.linux_section()
        assert 'download/' in redir

    @pytest.mark.UI
    def test_main_network_news(self, authorize):
        main_page = authorize
        redir = main_page.news_section()
        assert 'wireshark.org/news/' in redir

    @pytest.mark.UI
    def test_main_network_down(self, authorize):
        main_page = authorize
        redir = main_page.download_wireshark()
        assert 'wireshark.org/#download' in redir

    @pytest.mark.UI
    def test_main_network_exmp(self, authorize):
        main_page = authorize
        redir = main_page.examples()
        assert '/tcpdump-examples/' in redir

    @pytest.mark.UI
    def test_logout(self, authorize):
        main_page = authorize
        main_page.logout()
        assert main_page.isOut()

    @pytest.mark.UI
    def test_vk_id(self, db_setup):
        new = db_setup.add_user()
        requests.post(SET_USER, data={'user': new.username}, timeout=2)
        self.login_page.auth_with_text(new.username, new.password)
        assert self.main_page.idIsPresent()

    @pytest.mark.UI
    def test_neg_vk_id(self, db_setup):
        new = db_setup.add_user()
        login = new.username
        passwd = new.password
        self.login_page.auth_with_text(login, passwd)
        res = self.main_page.idIsPresent()
        db_setup.delete_user(new.id)
        assert not res

    @pytest.mark.UI
    def test_auth_with_no_access(self, db_setup):
        new = db_setup.add_user(access=False)
        login = new.username
        passwd = new.password
        self.login_page.auth_with_text(login, passwd)
        res = self.login_page.access_denied()
        db_setup.delete_user(new.id)
        assert res
