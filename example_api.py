##############
#    app.py  #
##############

from flask import Flask, render_template, Response
from v1_0 import v1_0

app = Flask(__name__)

app.register_blueprint(v1_0, url_prefix='/api/v1.0')


########################
#   v1_0/__init__.py   #
########################

from flask import Blueprint, make_response, jsonify, request
from flask_cors import cross_origin


v1_0 = Blueprint('v1_0', __name__)


class AppError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@v1_0.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


@v1_0.errorhandler(AppError)
def handle_app_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            # TODO: perform authentication here..
        except Exception as e:
            raise AuthError({"code": "authentication failed", "description": str(e)}, 401)
        return f(*args, **kwargs)
    return decorated


@v1_0.route('/my-endpoint', methods=['POST'])
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "*"])
@requires_auth
def endpoint_func():
    try:
        # TODO: business logic goes here..
        return make_response(jsonify({'Success': True}), 200)
    except Exception as e:
        raise AppError({"code": "product_term_error", "description": str(e)}, 500)
