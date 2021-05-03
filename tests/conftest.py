import pytest
import json
from flask import Flask, request, url_for
from flask.testing import FlaskClient
from manage import configure_env

# from application.wsgi import app
# from application.app import create_app


@pytest.fixture(scope='session')
def flask_app():

    configure_env('testing')
    flask_app = create_app('testing')

    with flask_app.app_context():

        yield flask_app
