from ui.ui_fixtures import *
from mysql_client.mysql_orm_client import MysqlOrmConnection
from mysql_client.orm_builder import MysqlOrmBuilder
from api.api_client import AppClient


@pytest.fixture(scope='session')
def mysql_client():
    return MysqlOrmConnection(user='root', password='root', db_name='test')


@pytest.fixture(scope='function')
def db_setup(mysql_client):
    mysql: MysqlOrmConnection = mysql_client
    yield MysqlOrmBuilder(connection=mysql)
    mysql.connection.close()


@pytest.fixture(scope='function')
def api_client():
    return AppClient()
