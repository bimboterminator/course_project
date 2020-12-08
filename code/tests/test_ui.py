import pytest
from _pytest.fixtures import FixtureRequest
import requests
import allure
from time import sleep
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

    @allure.title("user authorization")
    @pytest.mark.UI
    def test_auth(self, db_setup):
        """ Авторизация сущестующего пользователя.
                Заполнение формы авторизации.
                Переход на главную страницу"""
        new = db_setup.add_user()
        login = new.username
        passwd = new.password

        self.login_page.auth_with_text(login, passwd)
        is_displayed = self.login_page.login_isDisplayed(login)
        db_setup.delete_user(new.id)
        assert is_displayed

    @allure.title("Authorization of non-existent user")
    @pytest.mark.UI
    def test_auth_neg(self):
        """ Авторизация несуществующего пользоавтеля.
              Выдается сообщение об ошибке."""
        login = Faker().last_name() + '111'
        passwd = '192168'
        self.login_page.auth_with_text(login, passwd)
        is_displayed = self.login_page.error_isDisplayed()
        assert is_displayed

    @allure.title("Registration with short username")
    @pytest.mark.UI
    def test_reg_invalid_login_short(self):
        """Заполнение формы регистрации с коротким логином
            Поялвение сообщения с описанием невалидных данных"""
        login = 'pepe'
        email = Faker().email()
        passwd1 = '192168'
        passwd2 = '192168'
        self.reg_page.reg_with_text(login, email, passwd1, passwd2)
        assert self.reg_page.invalid_login()

    @allure.title("Registration with long username")
    @pytest.mark.UI
    def test_reg_invalid_login_long(self):
        """ Регистриация с длинным именем пользователя.
                Появление сообщения об ошибке"""
        login = 'pepesadasdasdasdasdasd'
        email = Faker().email()
        passwd1 = '192168'
        passwd2 = '192168'
        self.reg_page.reg_with_text(login, email, passwd1, passwd2)
        assert self.reg_page.invalid_login()

    @allure.title("Registration with invalid emal")
    @pytest.mark.UI
    def test_reg_invalid_email(self):
        """ Регистрицаия с невалидным email.
           Появление сообщени об ошибке.
           """
        login = Faker().last_name() + '666'
        email = 'mail@mail'
        passwd1 = '192168'
        passwd2 = '192168'
        self.reg_page.reg_with_text(login, email, passwd1, passwd2)
        assert self.reg_page.invalid_email()

    @allure.title("Registration with dublicated email")
    @pytest.mark.UI
    def test_reg_dublicated_email(self, db_setup):
        """ Регистрация с существующим email.
           Поялвение сообщения о существовании пользователя с такой почтой"""
        new = db_setup.add_user()
        login2 = Faker().first_name() + '666'
        email2 = new.email
        self.reg_page.reg_with_text(login2, email2, new.password, new.password)
        db_setup.delete_user(new.id)
        assert 'Such email already exists' == self.reg_page.email_exists(), "Wrong message: Internal server error, should be: email already exists"

    @allure.title("Registration with dublicated username")
    @pytest.mark.UI
    def test_reg_dublicated_username(self, db_setup):
        """Регистрация с существующим email.
            Появление сообщения о существовании такогопользователя"""
        new = db_setup.add_user()
        self.reg_page.reg_with_text(new.username, new.email, new.password, new.password)
        db_setup.delete_user(new.id)
        assert self.reg_page.user_exists()

    @allure.title("Registration with non mathching passwords")
    @pytest.mark.UI
    def test_reg_passw_notmatch(self):
        """ Регистриция с несовпадающими паролямм.
                Появление сообщения об ошибке."""
        login = Faker().first_name() + '666'
        email = 'mail@mail.com'
        passwd1 = '192'
        passwd2 = '192168'
        self.reg_page.reg_with_text(login, email, passwd1, passwd2)
        assert self.reg_page.pass_not_match()

    @allure.title("Registration with valid data")
    @pytest.mark.UI
    def test_reg_success(self):
        """Создание аккаунта с валидными данными.
                Ввод данных в поля регистрации.
                Login is displayed on main page
                """
        login = Faker().first_name() + '666'
        email = Faker().email()
        passwd1 = '192168'
        passwd2 = '192168'
        self.reg_page.reg_with_text(login, email, passwd1, passwd2)
        assert self.login_page.login_isDisplayed(login)

    @pytest.mark.UI
    def test_main_info_api(self, authorize):
        """Корректность ссылки на страницу с API.
                Нажатие на иконку под надписью "What is an API?".
                Новая вкладка с корректной страницей.
                """
        main_page = authorize
        redir = main_page.find_api()
        assert '/wiki/API' in redir

    @pytest.mark.UI
    def test_main_info_future(self, authorize):
        """Корректность ссылки на страницу с информацией о centos.
                Нажатие на иконку под надписью "Future of Internet".
                Новая вкладка с корректной страницей.
                """
        main_page = authorize
        redir = main_page.find_future()
        assert '/future-of-the-internet/' in redir

    @pytest.mark.UI
    def test_main_info_smtp(self, authorize):
        """Корректность ссылки на страницу с SMTP.
               Нажатие на иконку под надписью "Lets talk about SMTP?".
               Новая вкладка с корректной страницей.
               """
        main_page = authorize
        redir = main_page.find_smtp()
        assert '/wiki/SMTP' in redir

    @allure.title("Random fact on home page")
    @pytest.mark.UI
    def test_home_button(self, authorize):
        """ Отображение в нижней части страницы случайного мотивационного факта о python.
                Поиск объекта с данными.
                Факт присутствует.
                """
        main_page = authorize
        assert main_page.home_random_fact()

    @allure.title("Python main page")
    @pytest.mark.UI
    def test_main_python_redir(self, authorize):
        """Корректность ссылки на страницу питона.
                Нажатие на кпопку "Python".
                Новая вкладка с корректной страницей.
                """
        main_page = authorize
        redir = main_page.python_section()
        assert 'www.python.org' in redir, f"Deviation: {redir}"

    @allure.title("Python history page")
    @pytest.mark.UI
    def test_main_python_history(self, authorize):
        """Корректность ссылки на страницу с исторей питона.
                Нажатие на кпопку "Python history" в выдвигающемся меню.
                Новая вкладка с корректной страницей.
                """
        main_page = authorize
        redir = main_page.history_section()
        assert '/wiki/History_of_Python' in redir, f"Deviation: {redir}"

    @allure.title("Flask info page")
    @pytest.mark.UI
    def test_main_python_flask(self, authorize):
        """Корректность ссылки на страницу с информацией о flask.
                Нажатие на кпопку "About flask" в выдвигающемся меню.
                Новая вкладка с корректной страницей.
                """
        main_page = authorize
        redir = main_page.flask_section()
        assert 'flask' in redir, f"Deviation: {redir}"

    @allure.title("CentOS download page")
    @pytest.mark.UI
    def test_main_linux(self, authorize):
        """Корректность ссылки на страницу с информацией о centos.
               Нажатие на кпопку "Download centos7" в выдвигающемся меню.
               Новая вкладка с корректной страницей.
               """
        main_page = authorize
        redir = main_page.linux_section()
        assert 'download/' in redir

    @allure.title("Wireshark news")
    @pytest.mark.UI
    def test_main_network_news(self, authorize):
        """Корректность ссылки на страницу с новостями о wireshark.
                Нажатие на кпопку "wireshark news" в выдвигающемся меню.
                Новая вкладка с корректной страницей.
                """
        main_page = authorize
        redir = main_page.news_section()
        assert 'wireshark.org/news/' in redir

    @allure.title("Wireshark download")
    @pytest.mark.UI
    def test_main_network_down(self, authorize):
        """Корректность ссылки на страницу с установщиком wireshark.
                Нажатие на кпопку "wireshark download" в выдвигающемся меню.
                Новая вкладка с корректной страницей.
                """
        main_page = authorize
        redir = main_page.download_wireshark()
        assert 'wireshark.org/#download' in redir

    @allure.title("Wireshark news")
    @pytest.mark.UI
    def test_main_network_exmp(self, authorize):
        """Корректность ссылки на страницу с примерами TCP.
                Нажатие на кпопку "TCPDump Examples" в выдвигающемся меню.
                Новая вкладка с корректной страницей.
                """
        main_page = authorize
        redir = main_page.examples()
        assert '/tcpdump-examples/' in redir

    @allure.title("Logout test")
    @pytest.mark.UI
    def test_logout(self, authorize):
        """After pressing logout button user goes to login page"""
        main_page = authorize
        main_page.logout()
        assert main_page.isOut()

    @allure.title("VK ID is displayed")
    @pytest.mark.UI
    def test_vk_id(self, db_setup):
        """VK id IS dislplayed"""
        new = db_setup.add_user()
        requests.post(SET_USER, data={'user': new.username}, timeout=2)
        self.login_page.auth_with_text(new.username, new.password)
        assert self.main_page.idIsPresent()

    @allure.title("VK ID is NOT displayed")
    @pytest.mark.UI
    def test_neg_vk_id(self, db_setup):
        """VK id NOT dislplayed"""
        new = db_setup.add_user()
        login = new.username
        passwd = new.password
        self.login_page.auth_with_text(login, passwd)
        res = self.main_page.idIsPresent()
        db_setup.delete_user(new.id)
        assert not res

    @allure.title("AUTHORIZATION of blocked user")
    @pytest.mark.UI
    def test_auth_with_no_access(self, db_setup):
        """AUTHORIZATION of blocked user. Messege that user's blocked is displayed"""
        new = db_setup.add_user(access=False)
        login = new.username
        passwd = new.password
        self.login_page.auth_with_text(login, passwd)
        res = self.login_page.access_denied()
        db_setup.delete_user(new.id)
        assert res

    @allure.title("Масшатбируемость главной страницы")
    @pytest.mark.UI
    def test_window_size(self, authorize):
        """ Масшатбируемость главной страницы
                Элементы верхнего меню дoлжны быть видимы
        """
        main_page = authorize
        self.driver.set_window_size(350, 750)
        sleep(3)
        status = main_page.find(main_page.locators.HOME).is_displayed()
        assert status, 'Top menubar disappeared'
