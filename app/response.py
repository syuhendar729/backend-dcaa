from flask import jsonify, make_response

def success(value, message):
    res = {
            'data':value,
            'message': message
    }
    return make_response(jsonify(res)), 200

def badRequest(values, message):
    res = {
        'data' : values,
        'message': message
    }

    return make_response(jsonify(res)), 400

def serverError(values, message):
    res = {
        'data' : values,
        'message': message
    }

    return make_response(jsonify(res)), 500
