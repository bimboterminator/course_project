import threading
from random import randint
from flask import Flask, request, jsonify


app = Flask(__name__)

VK_HOST, VK_PORT = '0.0.0.0', 1052
VK_URL = f'http://{VK_HOST}:{VK_PORT}'

class Users:
    users = []
    ids = {}


def run_app():
    server = threading.Thread(target=app.run, kwargs={
        'host': VK_HOST,
        'port': VK_PORT
    })

    server.start()
    return server


# Добавляем точку завершения приложения, чтобы мы могли его при необходимостм правильно закрыть
def shutdown_app():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_app()
    return 'OK'


@app.route('/vk_id/<username>')
def vkid(username):
    if request.method == 'GET':
        if username in Users.users:
            return jsonify({'vk_id': Users.ids[username]}), 200
        else:
            return jsonify({}), 404


@app.route('/set_user', methods=['POST'])
def set_valid_users():
    if request.method == 'POST':
        user = request.form['user']
        Users.users.append(user)
        Users.ids[user] = randint(100, 10000)
        return {'users': f'User  was set'}


if __name__ == '__main__':
    run_app()
