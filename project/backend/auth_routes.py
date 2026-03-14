from flask import Blueprint, request, jsonify
from db import connect_db
import jwt
import datetime

auth_bp = Blueprint("auth", __name__)

SECRET_KEY = "mysecret"

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.json

    username = data["username"]
    password = data["password"]

    db = connect_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password)
    )

    user = cursor.fetchone()

    if not user:
        return jsonify({"error": "Invalid login"}), 401

    token = jwt.encode(
        {
            "user_id": user["id"],
            "role": user["role"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        },
        SECRET_KEY
    )

    return jsonify({"token": token})