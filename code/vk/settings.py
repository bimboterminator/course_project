from urllib.parse import urljoin


APP_HOST, APP_PORT = '0.0.0.0', 8080
APP_URL = f'http://{APP_HOST}:{APP_PORT}'
LOGIN_URL = urljoin(APP_URL, 'login')
REG_URL = urljoin(APP_URL, 'reg')
ADD_USR = urljoin(APP_URL, 'api/add_user')
DEL_USR = urljoin(APP_URL, 'api/del_user')
API_URL = urljoin(APP_URL, 'api')
API_BLOCK = urljoin(API_URL, 'block_user')
STATUS = urljoin(APP_URL, 'status')

VK_HOST, VK_PORT = '0.0.0.0', 1052
VK_URL = f'http://{VK_HOST}:{VK_PORT}'
SET_USER = urljoin(VK_URL, 'set_user')


