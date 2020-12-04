import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage
from ui.pages.reg_page import RegPage
from ui.pages.main_page import MainPage



class UsupportedBrowserException(Exception):
    pass


def pytest_addoption(parser):
    parser.addoption('--url', default='http://0.0.0.0:8080/')
    parser.addoption('--browser', default='Chrome')
    parser.addoption('--browser_ver', default='latest')
    parser.addoption('--selenoid', default=None)


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    browser = request.config.getoption('--browser')
    version = request.config.getoption('--browser_ver')
    selenoid = request.config.getoption('--selenoid')
    return {'browser': browser, 'version': version, 'url': url, 'selenoid': selenoid}


@pytest.fixture(scope='function')
def driver(config):
    browser = config['browser']
    version = config['version']
    url = config['url']
    selenoid = config['selenoid']
    if not selenoid:
        if browser == 'Chrome':
            manager = ChromeDriverManager(version=version)
            driver = webdriver.Chrome(executable_path=manager.install())
        elif browser == 'firefox':
            manager = GeckoDriverManager(version=version)
            driver = webdriver.Firefox(executable_path=manager.install())

        else:
            raise UsupportedBrowserException(f'Usupported browser: "{browser}"')
    else:
        options = ChromeOptions()
        capabilities = {'acceptInsecureCerts': True,
                        'browserName': 'chrome',
                        'version': '86.0'}
        driver = webdriver.Remote(command_executor=selenoid,
                                  desired_capabilities=capabilities)
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture
def reg_page(driver):
    return RegPage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)



