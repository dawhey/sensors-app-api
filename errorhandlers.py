from sensorsapi import app
from models import ValidationError, ApiError, AuthorizationError
from flask import jsonify


@app.errorhandler(ValidationError)
def bad_request(e):
    error = ApiError(400, 'bad request', e.args[0])
    return get_response_from_error(error)


@app.errorhandler(404)
def not_found(e):
    error = ApiError(404, 'not found', 'requested URI does not exist')
    return get_response_from_error(error)


@app.errorhandler(AuthorizationError)
def unauthorized(e):
    error = ApiError(401, 'unauthorized', e.args[0])
    return get_response_from_error(error)


@app.errorhandler(500)
def internal_error(e):
    error = ApiError(500, 'internal error', e.args[0])
    return get_response_from_error(error)


@app.errorhandler(405)
def unsupported_method(e):
    error = ApiError(405, 'not supported', 'requested method is not supported')
    return get_response_from_error(error)


def get_response_from_error(error):
    response = jsonify(error.export())
    response.status_code = error.status
    return response
