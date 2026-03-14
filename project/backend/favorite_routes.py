from flask import Blueprint, request, jsonify
from db import connect_db
from middleware_auth import verify_token

favorite_bp = Blueprint("favorite", __name__)

@favorite_bp.route("/favorites", methods=["POST"])
def add_favorite():

    user = verify_token()

    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json

    db = connect_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO favorites(user_id,store_id) VALUES(%s,%s)",
        (user["user_id"], data["store_id"])
    )

    db.commit()

    return jsonify({"message": "favorite added"})


@favorite_bp.route("/favorites", methods=["GET"])
def get_favorites():

    user = verify_token()

    db = connect_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM favorites WHERE user_id=%s",
        (user["user_id"],)
    )

    return jsonify(cursor.fetchall())