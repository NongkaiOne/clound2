from flask import request, jsonify
import jwt

SECRET_KEY = "mysecret"

def verify_token():
    token = request.headers.get("Authorization")

    if not token:
        return None

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return data
    except:
        return None


def require_role(role):
    def decorator(func):
        def wrapper(*args, **kwargs):

            user = verify_token()

            if not user:
                return jsonify({"error": "Unauthorized"}), 401

            if user["role"] != role:
                return jsonify({"error": "Forbidden"}), 403

            return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        return wrapper
    return decorator