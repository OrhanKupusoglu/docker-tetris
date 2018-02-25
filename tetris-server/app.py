"""
    Tetris Server
    Flask:
    http://flask.pocoo.org/
    Tetris:
    https://github.com/ytiurin/tetris
"""

import os
import uuid
import time
import logging
import logging.handlers
import json
from flask import (
    abort,
    Flask,
    request,
    Response,
    session,
    g,
    jsonify,
    redirect,
    url_for,
    abort,
    render_template,
    flash,
)

# APP

app = Flask(__name__, static_folder='static', static_url_path='')

app.config.update(dict(
    SECRET_KEY = str(uuid.uuid4()),
    LOG_ENABLED = True,
    LOG_LEVEL = 'INFO',
    LOG_FILE = 'tetris-server/static/log/server.txt',
    LOG_MAX_BYTES = 1024 * 1024,
    LOG_BACKUP_COUNT = 10,
    SHUTDOWN_IF_LOCALHOST_ONLY = True
))

app.config.from_envvar('TETRIS_SERVER_SETTINGS', silent=True)

# LOGGER

if app.config['LOG_ENABLED']:
    logHandler = logging.handlers.RotatingFileHandler(app.config['LOG_FILE'],
                                                      maxBytes=app.config['LOG_MAX_BYTES'],
                                                      backupCount=app.config['LOG_BACKUP_COUNT'])
    logHandler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s"))

    if app.config['LOG_LEVEL'] == 'DEBUG':
        app.logger.setLevel(logging.DEBUG)
    elif app.config['LOG_LEVEL'] == 'INFO':
        app.logger.setLevel(logging.INFO)
    elif app.config['LOG_LEVEL'] == 'WARNING':
        app.logger.setLevel(logging.WARNING)
    elif app.config['LOG_LEVEL'] == 'ERROR':
        app.logger.setLevel(logging.ERROR)
    elif app.config['LOG_LEVEL'] == 'CRITICAL':
        app.logger.setLevel(logging.CRITICAL)

    app.logger.addHandler(logHandler)
    logging.getLogger('werkzeug').addHandler(logHandler)

    with open(app.config['LOG_FILE'], 'a') as log_file:
        log_file.write('\n' + 80*'-' + '\n\n')
else:
    app.logger.disabled = True
    logging.getLogger('werkzeug').disabled = True

app.logger.info('Application started')

# HELPER FUNCTIONS

def is_localhost():
    remote_addr = request.environ['REMOTE_ADDR']
    app.logger.info('request - remote addr = {}'.format(remote_addr))
    return remote_addr == '127.0.0.1' or remote_addr == '::1'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('not running with the Werkzeug Server')
    func()

# ROUTES

@app.route('/')
def show_root():
    app.logger.info('URL: {} - client: {}\n\t{}'.format(request.url, request.remote_addr, request.headers.get('User-Agent')))
    return redirect(url_for('show_game'))

@app.route('/tetris')
def show_game():
    return redirect(url_for('get_game', file='index.html'))

@app.route('/tetris/<path:file>')
def get_game(file):
    app.logger.info('URL: {} - client: {}\n\t{}'.format(request.url, request.remote_addr, request.headers.get('User-Agent')))
    return app.send_static_file('tetris/' + file)

@app.route('/log')
def show_log():
    app.logger.info('URL: {} - client: {}\n\t{}'.format(request.url, request.remote_addr, request.headers.get('User-Agent')))
    return app.send_static_file('log/server.txt')

@app.route('/shutdown', methods=['POST'])
def shutdown():
    app.logger.info('URL: {} - client: {}\n\t{}'.format(request.url, request.remote_addr, request.headers.get('User-Agent')))

    if app.config['SHUTDOWN_IF_LOCALHOST_ONLY']:
        if not is_localhost():
            abort(401)

    shutdown_server()
    return 'Service shutting down...'

# ERRORS

@app.errorhandler(401)
def unauthorized(error=None):
    message = {'status': 401,
               'message': 'Unauthorized',
               'url': request.url}

    resp = jsonify(message)
    resp.status_code = 401
    return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {'status': 404,
               'message': 'Not Found',
               'url': request.url}

    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.errorhandler(500)
def not_found(error=None):
    message = {'status': 500,
               'message': 'Internal Server Error',
               'url': request.url}

    resp = jsonify(message)
    resp.status_code = 500
    return resp
